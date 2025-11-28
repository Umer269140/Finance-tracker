import firebase_config
from .. import local_data
from ..transactions import transactions as t # Import transactions for summary

def set_budget(user_id, id_token, is_admin, category, amount):
    """Sets a monthly budget for a user (local for admin, Firebase for others)."""
    if is_admin:
        local_data.set_local_budget(user_id, category, amount)
    else:
        if not firebase_config.db:
            raise Exception("Firebase Realtime Database not configured.")
        
        budget_data = {
            'category': category,
            'amount': amount
        }
        
        firebase_config.db.child("budgets").child(user_id).child(category).set(budget_data, token=id_token)
        print(f"Budget for {category} set to {amount}")

def get_budgets(user_id, id_token, is_admin):
    """Retrieves all budgets for a user (local for admin, Firebase for others)."""
    if is_admin:
        return local_data.get_local_budgets(user_id)
    else:
        if not firebase_config.db:
            return []
        try:
            budgets_ref = firebase_config.db.child("budgets").child(user_id).get(token=id_token)
            if budgets_ref.val():
                budgets = [item.val() for item in budgets_ref.each()]
                return budgets
            return []
        except Exception as e:
            print(f"Could not get budgets: {e}")
            return []

def get_budget_summary(user_id, id_token, is_admin):
    """Calculates the budget summary for a user (local for admin, Firebase for others)."""
    if is_admin:
        budgets = local_data.get_local_budgets(user_id)
        transactions = local_data.get_all_local_transactions(user_id)
    else:
        budgets = get_budgets(user_id, id_token, is_admin) # Ensure this calls Firebase version
        transactions = t.get_all_transactions(user_id, id_token, is_admin) # Ensure this calls Firebase version
    
    budget_details = []
    total_budget_amount = 0
    total_spent_amount = 0

    if not isinstance(budgets, list):
        budgets = []
        
    for budget in budgets:
        category = budget.get('category')
        budget_amount = budget.get('amount', 0)
        
        spent = sum(
            trans.get('amount', 0) 
            for trans in transactions 
            if trans.get('type') == 'Expense' and trans.get('name') == category
        )
        
        remaining = budget_amount - spent
        utilization_percent = (spent / budget_amount) * 100 if budget_amount > 0 else 0
        
        status = "OK"
        if utilization_percent > 100:
            status = "Over"
        elif utilization_percent > 70:
            status = "Warning"
            
        budget_details.append({
            "category": category,
            "budget_amount": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "utilization_percent": utilization_percent,
            "status": status
        })
        
        total_budget_amount += budget_amount
        total_spent_amount += spent

    overall_remaining = total_budget_amount - total_spent_amount
    overall_utilization_percent = (total_spent_amount / total_budget_amount) * 100 if total_budget_amount > 0 else 0
    
    categories_over_budget = [item['category'] for item in budget_details if item['status'] == 'Over']

    return {
        "budget_details": budget_details,
        "total_budget_amount": total_budget_amount,
        "total_spent_amount": total_spent_amount,
        "overall_remaining": overall_remaining,
        "overall_utilization_percent": overall_utilization_percent,
        "categories_over_budget": categories_over_budget
    }
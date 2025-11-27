import firebase_config
from features.transactions import transactions as t

def set_budget(user_id, category, amount):
    """Sets a monthly budget for a user in the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")
    
    budget_data = {
        'category': category,
        'amount': amount
    }
    
    # Set the budget for a user and category
    firebase_config.db.child("budgets").child(user_id).child(category).set(budget_data)
    print(f"Budget for {category} set to {amount}")

def get_budgets(user_id):
    """Retrieves all budgets for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return []
        
    budgets_ref = firebase_config.db.child("budgets").child(user_id).get()
    if budgets_ref.val():
        # The result from get() is a Pyrebase object, we need to convert it to a list of dicts
        budgets = [item.val() for item in budgets_ref.each()]
        return budgets
    return []

def get_budget_summary(user_id):
    """Calculates the budget summary for a user."""
    budgets = get_budgets(user_id)
    transactions = t.get_all_transactions(user_id)
    
    budget_details = []
    total_budget_amount = 0
    total_spent_amount = 0

    # Ensure budgets is a list of dictionaries
    if not isinstance(budgets, list):
        budgets = []
        
    for budget in budgets:
        category = budget.get('category')
        budget_amount = budget.get('amount', 0)
        
        # This assumes transaction amounts are stored as numbers
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
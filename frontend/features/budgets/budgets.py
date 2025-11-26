# Functions for budget management
from firebase_config import db
from features.transactions import transactions as t

def set_budget(user_id, category, amount):
    """Sets a monthly budget for a user in the Firestore database."""
    if not db:
        print("Error: Firestore database not initialized.")
        return
        
    try:
        doc_ref = db.collection('budgets').document(f"{user_id}_{category}")
        doc_ref.set({
            'user_id': user_id,
            'category': category,
            'amount': amount
        })
        print(f"Budget for {category} set to {amount}")
    except Exception as e:
        print(f"Error setting budget: {e}")

def get_budgets(user_id):
    """Retrieves all budgets for a user from the Firestore database."""
    if not db:
        print("Error: Firestore database not initialized.")
        return []
        
    try:
        budgets = []
        docs = db.collection('budgets').where('user_id', '==', user_id).stream()
        for doc in docs:
            budgets.append(doc.to_dict())
        return budgets
    except Exception as e:
        print(f"Error getting budgets: {e}")
        return []

def get_budget_summary(user_id):
    """Calculates the budget summary for a user."""
    if not db:
        print("Error: Firestore database not initialized.")
        return {
            "budget_details": [],
            "total_budget_amount": 0,
            "total_spent_amount": 0,
            "overall_remaining": 0,
            "overall_utilization_percent": 0,
            "categories_over_budget": []
        }
        
    budgets = get_budgets(user_id)
    transactions = t.get_all_transactions(user_id)
    
    budget_details = []
    total_budget_amount = 0
    total_spent_amount = 0

    for budget in budgets:
        category = budget['category']
        budget_amount = budget['amount']
        spent = sum(trans['amount'] for trans in transactions if trans['type'] == 'Expense' and trans['category'] == category)
        
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

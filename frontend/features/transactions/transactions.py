import firebase_config
from datetime import datetime
import uuid

def add_transaction(user_id, transaction_type, amount, date, name, description, billing_number, payment_method):
    """Adds a new transaction to the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")
    
    transaction_id = str(uuid.uuid4())
    transaction_data = {
        'id': transaction_id,
        'type': transaction_type,
        'amount': amount,
        'date': date,
        'name': name,
        'description': description,
        'billing_number': billing_number,
        'payment_method': payment_method
    }
    
    # Push the data to a user-specific path
    firebase_config.db.child("transactions").child(user_id).child(transaction_id).set(transaction_data)
    print(f"Transaction added with ID: {transaction_id}")

def get_all_transactions(user_id):
    """Retrieves all transactions for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return []
        
    transactions_ref = firebase_config.db.child("transactions").child(user_id).get()
    if transactions_ref:
        # The result from get() is a Pyrebase object, we need to convert it to a list of dicts
        transactions = [item.val() for item in transactions_ref.each()]
        return transactions
    return []

def delete_transaction(user_id, transaction_id):
    """Deletes a transaction from the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")

    firebase_config.db.child("transactions").child(user_id).child(transaction_id).remove()
    print(f"Transaction with ID {transaction_id} deleted successfully.")


def get_financial_summary(user_id):
    """Calculates total income, total expenses, and current balance for a user."""
    transactions = get_all_transactions(user_id)
    total_income = sum(trans["amount"] for trans in transactions if trans["type"] == "Income")
    total_expenses = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")
    current_balance = total_income - total_expenses
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance
    }

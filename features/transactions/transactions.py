import firebase_config
from datetime import datetime
import uuid

def add_transaction(session_state, user_id, id_token, is_admin, transaction_type, amount, date, name, description, billing_number, payment_method):
    """Adds a new transaction to the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")
    
    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")

    transaction_id = str(uuid.uuid4())
    transaction_data = {
        'type': transaction_type,
        'amount': amount,
        'date': date,
        'name': name,
        'description': description,
        'billing_number': billing_number,
        'payment_method': payment_method
    }
    
    firebase_config.db.child("transactions").child(user_id).child(transaction_id).set(transaction_data, token=id_token)
    print(f"Transaction added with ID: {transaction_id}")

def get_all_transactions(session_state, user_id, id_token, is_admin):
    """Retrieves all transactions for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return []
    
    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        # If token refresh fails, assume not logged in or session expired
        return []
    try:
        transactions_ref = firebase_config.db.child("transactions").child(user_id).get(token=id_token)
        if transactions_ref.val():
            transactions = []
            for item in transactions_ref.each():
                transaction = item.val()
                transaction['id'] = item.key() # Add the ID from the Firebase key
                transactions.append(transaction)
            return transactions
        return []
    except Exception as e:
        print(f"Could not get transactions: {e}")
        return []

def delete_transaction(session_state, user_id, id_token, is_admin, transaction_id):
    """Deletes a transaction from the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")

    firebase_config.db.child("transactions").child(user_id).child(transaction_id).remove(token=id_token)
    print(f"Transaction with ID {transaction_id} deleted successfully.")


def get_financial_summary(session_state, user_id, id_token, is_admin):
    """Calculates total income, total expenses, and current balance for a user from Firebase."""
    transactions = get_all_transactions(session_state, user_id, id_token, is_admin) # Pass session_state
    total_income = sum(trans["amount"] for trans in transactions if trans["type"] == "Income")
    total_expenses = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")
    current_balance = total_income - total_expenses
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance
    }

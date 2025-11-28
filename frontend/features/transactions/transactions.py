import firebase_config
from datetime import datetime
import uuid
import frontend.features.local_data as local_data # Import local data functions

def add_transaction(user_id, id_token, is_admin, transaction_type, amount, date, name, description, billing_number, payment_method):
    """Adds a new transaction to the database (local for admin, Firebase for others)."""
    if is_admin:
        local_data.add_local_transaction(user_id, transaction_type, amount, date, name, description, billing_number, payment_method)
    else:
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
        
        firebase_config.db.child("transactions").child(user_id).child(transaction_id).set(transaction_data, token=id_token)
        print(f"Transaction added with ID: {transaction_id}")

def get_all_transactions(user_id, id_token, is_admin):
    """Retrieves all transactions for a user (local for admin, Firebase for others)."""
    if is_admin:
        return local_data.get_all_local_transactions(user_id)
    else:
        if not firebase_config.db:
            return []
        try:
            transactions_ref = firebase_config.db.child("transactions").child(user_id).get(token=id_token)
            if transactions_ref.val():
                transactions = [item.val() for item in transactions_ref.each()]
                return transactions
            return []
        except Exception as e:
            print(f"Could not get transactions: {e}")
            return []

def delete_transaction(user_id, id_token, is_admin, transaction_id):
    """Deletes a transaction from the database (local for admin, Firebase for others)."""
    if is_admin:
        local_data.delete_local_transaction(user_id, transaction_id)
    else:
        if not firebase_config.db:
            raise Exception("Firebase Realtime Database not configured.")

        firebase_config.db.child("transactions").child(user_id).child(transaction_id).remove(token=id_token)
        print(f"Transaction with ID {transaction_id} deleted successfully.")


def get_financial_summary(user_id, id_token, is_admin):
    """Calculates total income, total expenses, and current balance for a user (local for admin, Firebase for others)."""
    if is_admin:
        return local_data.get_local_financial_summary(user_id)
    else:
        transactions = get_all_transactions(user_id, id_token, is_admin=False) # Ensure this calls Firebase version
        total_income = sum(trans["amount"] for trans in transactions if trans["type"] == "Income")
        total_expenses = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")
        current_balance = total_income - total_expenses
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "current_balance": current_balance
        }

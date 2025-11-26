import csv
import os
import uuid
from datetime import datetime

# Define the path to the transactions CSV file
TRANSACTIONS_FILE = os.path.join(os.path.dirname(__file__), '../../../database/transactions.csv')

# Ensure the database directory exists
os.makedirs(os.path.dirname(TRANSACTIONS_FILE), exist_ok=True)

def _read_transactions_from_csv():
    """Reads all transactions from the CSV file."""
    transactions = []
    if not os.path.exists(TRANSACTIONS_FILE):
        return transactions

    with open(TRANSACTIONS_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert amount back to float/int if needed, ensure consistent types
            row['amount'] = float(row['amount'])
            transactions.append(row)
    return transactions

def _write_transactions_to_csv(transactions):
    """Writes a list of transactions to the CSV file."""
    if not transactions:
        # Create an empty file with headers if no transactions
        headers = ['id', 'user_id', 'type', 'amount', 'date', 'name', 'description', 'billing_number', 'payment_method']
        with open(TRANSACTIONS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
        return

    # Assuming all transactions have the same keys, use the first one for headers
    headers = list(transactions[0].keys())
    with open(TRANSACTIONS_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transactions)

def add_transaction(user_id, transaction_type, amount, date, name, description, billing_number, payment_method):
    """Adds a new transaction to the CSV file."""
    transactions = _read_transactions_from_csv()
    new_transaction = {
        'id': str(uuid.uuid4()), # Generate a unique ID
        'user_id': user_id,
        'type': transaction_type,
        'amount': amount,
        'date': date,
        'name': name,
        'description': description,
        'billing_number': billing_number,
        'payment_method': payment_method
    }
    transactions.append(new_transaction)
    _write_transactions_to_csv(transactions)
    print(f"Transaction added with ID: {new_transaction['id']}")

def get_all_transactions(user_id):
    """Retrieves all transactions for a user from the CSV file."""
    all_transactions = _read_transactions_from_csv()
    return [trans for trans in all_transactions if trans['user_id'] == user_id]

def delete_transaction(transaction_id):
    """Deletes a transaction from the CSV file."""
    transactions = _read_transactions_from_csv()
    initial_count = len(transactions)
    transactions = [trans for trans in transactions if trans['id'] != transaction_id]
    if len(transactions) < initial_count:
        _write_transactions_to_csv(transactions)
        print(f"Transaction with ID {transaction_id} deleted successfully.")
    else:
        print(f"Transaction with ID {transaction_id} not found.")

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
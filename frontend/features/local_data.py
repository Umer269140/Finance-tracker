import csv
import json
import os
import uuid
from datetime import datetime

# Define file paths
TRANSACTIONS_FILE = os.path.join(os.path.dirname(__file__), '../../../database/transactions.csv')
BUDGETS_FILE = os.path.join(os.path.dirname(__file__), '../../../database/budgets.txt')
LEDGERS_FILE = os.path.join(os.path.dirname(__file__), '../../../database/ledgers.json')

# Ensure database directory exists
os.makedirs(os.path.dirname(TRANSACTIONS_FILE), exist_ok=True)

# --- Transactions (CSV) ---
def _read_transactions_from_csv():
    transactions = []
    if not os.path.exists(TRANSACTIONS_FILE) or os.stat(TRANSACTIONS_FILE).st_size == 0:
        return transactions

    with open(TRANSACTIONS_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['amount'] = float(row['amount'])
            transactions.append(row)
    return transactions

def _write_transactions_to_csv(transactions):
    if not transactions:
        headers = ['id', 'user_id', 'type', 'amount', 'date', 'name', 'description', 'billing_number', 'payment_method']
        with open(TRANSACTIONS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
        return

    headers = list(transactions[0].keys())
    with open(TRANSACTIONS_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transactions)

def add_local_transaction(user_id, transaction_type, amount, date, name, description, billing_number, payment_method):
    transactions = _read_transactions_from_csv()
    new_transaction = {
        'id': str(uuid.uuid4()),
        'user_id': user_id, # This will be the admin's fixed user_id
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
    print(f"Local Transaction added with ID: {new_transaction['id']}")

def get_all_local_transactions(user_id):
    all_transactions = _read_transactions_from_csv()
    return [trans for trans in all_transactions if trans['user_id'] == user_id]

def delete_local_transaction(user_id, transaction_id):
    transactions = _read_transactions_from_csv()
    initial_count = len(transactions)
    transactions = [trans for trans in transactions if not (trans['id'] == transaction_id and trans['user_id'] == user_id)]
    if len(transactions) < initial_count:
        _write_transactions_to_csv(transactions)
        print(f"Local Transaction with ID {transaction_id} deleted successfully.")
    else:
        print(f"Local Transaction with ID {transaction_id} not found.")

def get_local_financial_summary(user_id):
    transactions = get_all_local_transactions(user_id)
    total_income = sum(trans["amount"] for trans in transactions if trans["type"] == "Income")
    total_expenses = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")
    current_balance = total_income - total_expenses
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance
    }

# --- Budgets (Text file) ---
def _read_budgets_from_file():
    budgets = []
    if not os.path.exists(BUDGETS_FILE) or os.stat(BUDGETS_FILE).st_size == 0:
        return budgets
    
    with open(BUDGETS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'): # Ignore comments and empty lines
                try:
                    category, amount_str = line.split('=', 1)
                    budgets.append({'category': category.strip(), 'amount': float(amount_str.strip())})
                except ValueError:
                    print(f"Warning: Skipping malformed budget line: {line}")
    return budgets

def _write_budgets_to_file(budgets):
    with open(BUDGETS_FILE, 'w', encoding='utf-8') as f:
        for budget in budgets:
            f.write(f"{budget['category']}={budget['amount']}\n")

def set_local_budget(user_id, category, amount):
    budgets = _read_budgets_from_file()
    found = False
    for budget in budgets:
        if budget['category'] == category:
            budget['amount'] = amount
            found = True
            break
    if not found:
        budgets.append({'user_id': user_id, 'category': category, 'amount': amount})
    _write_budgets_to_file(budgets)
    print(f"Local budget for {category} set to {amount}")

def get_local_budgets(user_id):
    # For local budgets, we're assuming they are global for the admin or specific to a fixed user_id
    # If the user_id is part of the budget entry, filter by it.
    all_budgets = _read_budgets_from_file()
    return [b for b in all_budgets if b.get('user_id') == user_id]

def get_local_budget_summary(user_id):
    budgets = get_local_budgets(user_id)
    transactions = get_all_local_transactions(user_id) # Use local transactions for summary
    
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

# --- Ledgers (JSON) ---
def _read_ledgers_from_json():
    ledgers = []
    if not os.path.exists(LEDGERS_FILE) or os.stat(LEDGERS_FILE).st_size == 0:
        return ledgers
    with open(LEDGERS_FILE, mode='r', encoding='utf-8') as file:
        try:
            ledgers = json.load(file)
        except json.JSONDecodeError:
            ledgers = []
    return ledgers

def _write_ledgers_to_json(ledgers):
    with open(LEDGERS_FILE, mode='w', encoding='utf-8') as file:
        json.dump(ledgers, file, indent=4)

def add_local_ledger_account(user_id, account_name):
    ledgers = _read_ledgers_from_json()
    if any(l['user_id'] == user_id and l['account_name'] == account_name for l in ledgers):
        return False
        
    new_account = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'account_name': account_name,
        'entries': []
    }
    ledgers.append(new_account)
    _write_ledgers_to_json(ledgers)
    return True

def get_all_local_ledger_accounts(user_id):
    ledgers = _read_ledgers_from_json()
    return [l for l in ledgers if l['user_id'] == user_id]

def get_local_ledger_account_by_id(user_id, account_id):
    ledgers = _read_ledgers_from_json()
    for ledger in ledgers:
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            return ledger
    return None

def get_local_ledger_account_by_name(user_id, account_name):
    ledgers = _read_ledgers_from_json()
    for ledger in ledgers:
        if ledger['user_id'] == user_id and ledger['account_name'] == account_name:
            return ledger
    return None

def add_local_entry_to_ledger_account(user_id, account_id, transaction_name, description, transaction_type, billing_number, amount, payment_method):
    ledgers = _read_ledgers_from_json()
    for i, ledger in enumerate(ledgers):
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            entry_type = "Debit" if transaction_type == "Expense" else "Credit"
            new_entry = {
                "name": transaction_name,
                "description": description,
                "type": entry_type,
                "amount": float(amount),
                "billing_number": billing_number,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "paid": False,
                "payment_method": payment_method
            }
            ledgers[i]['entries'].append(new_entry)
            _write_ledgers_to_json(ledgers)
            return True
    return False

def delete_local_entry_from_ledger_account(user_id, account_id, entry_index):
    ledgers = _read_ledgers_from_json()
    for i, ledger in enumerate(ledgers):
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            if 0 <= entry_index < len(ledgers[i]['entries']):
                del ledgers[i]['entries'][entry_index]
                _write_ledgers_to_json(ledgers)
                return True
    return False

def mark_local_ledger_entry_paid(user_id, account_id, entry_index, paid_status):
    ledgers = _read_ledgers_from_json()
    for i, ledger in enumerate(ledgers):
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            if 0 <= entry_index < len(ledgers[i]['entries']):
                ledgers[i]['entries'][entry_index]['paid'] = paid_status
                _write_ledgers_to_json(ledgers)
                return True
    return False

def delete_local_ledger_account(user_id, account_id):
    ledgers = _read_ledgers_from_json()
    initial_count = len(ledgers)
    ledgers = [l for l in ledgers if not (l['id'] == account_id and l['user_id'] == user_id)]
    if len(ledgers) < initial_count:
        _write_ledgers_to_json(ledgers)
        return True
    return False

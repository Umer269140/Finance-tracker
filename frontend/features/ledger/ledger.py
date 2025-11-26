import json
import os
import uuid
from datetime import datetime

# Define the path to the ledgers JSON file
LEDGERS_FILE = os.path.join(os.path.dirname(__file__), '../../../database/ledgers.json')

# Ensure the database directory exists
os.makedirs(os.path.dirname(LEDGERS_FILE), exist_ok=True)

def _read_ledgers_from_json():
    """Reads all ledger accounts from the JSON file."""
    ledgers = []
    if os.path.exists(LEDGERS_FILE):
        with open(LEDGERS_FILE, mode='r', encoding='utf-8') as file:
            try:
                ledgers = json.load(file)
            except json.JSONDecodeError:
                ledgers = [] # Return empty list if file is empty or corrupted
    return ledgers

def _write_ledgers_to_json(ledgers):
    """Writes a list of ledger accounts to the JSON file."""
    with open(LEDGERS_FILE, mode='w', encoding='utf-8') as file:
        json.dump(ledgers, file, indent=4)

def add_ledger_account(user_id, account_name):
    """Adds a new empty ledger account."""
    ledgers = _read_ledgers_from_json()
    
    # Check if an account with the same name already exists for this user
    if any(l['user_id'] == user_id and l['account_name'] == account_name for l in ledgers):
        return False # Account already exists, do not create
        
    new_account = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'account_name': account_name,
        'entries': []
    }
    ledgers.append(new_account)
    _write_ledgers_to_json(ledgers)
    return True

def get_all_ledger_accounts(user_id):
    """Retrieves all ledger accounts for a user."""
    ledgers = _read_ledgers_from_json()
    return [l for l in ledgers if l['user_id'] == user_id]

def get_ledger_account_by_id(user_id, account_id):
    """Retrieves a single ledger account by its ID for a user."""
    ledgers = _read_ledgers_from_json()
    for ledger in ledgers:
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            return ledger
    return None

def get_ledger_account_by_name(user_id, account_name):
    """Retrieves a single ledger account by its name for a user."""
    ledgers = _read_ledgers_from_json()
    for ledger in ledgers:
        if ledger['user_id'] == user_id and ledger['account_name'] == account_name:
            return ledger
    return None

def add_entry_to_ledger_account(user_id, account_id, transaction_name, description, transaction_type, billing_number, amount, payment_method):
    """Adds a new entry to a specific ledger account."""
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
                "paid": False, # Default paid status
                "payment_method": payment_method
            }
            ledgers[i]['entries'].append(new_entry)
            _write_ledgers_to_json(ledgers)
            return True
    return False

def delete_entry_from_ledger_account(user_id, account_id, entry_index):
    """Deletes an entry from a specific ledger account by its index."""
    ledgers = _read_ledgers_from_json()
    for i, ledger in enumerate(ledgers):
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            if 0 <= entry_index < len(ledgers[i]['entries']):
                del ledgers[i]['entries'][entry_index]
                _write_ledgers_to_json(ledgers)
                return True
    return False

def mark_ledger_entry_paid(user_id, account_id, entry_index, paid_status):
    """Marks a ledger entry as paid or unpaid."""
    ledgers = _read_ledgers_from_json()
    for i, ledger in enumerate(ledgers):
        if ledger['id'] == account_id and ledger['user_id'] == user_id:
            if 0 <= entry_index < len(ledgers[i]['entries']):
                ledgers[i]['entries'][entry_index]['paid'] = paid_status
                _write_ledgers_to_json(ledgers)
                return True
    return False

def delete_ledger_account(user_id, account_id):
    """Deletes a ledger account by its ID."""
    ledgers = _read_ledgers_from_json()
    initial_count = len(ledgers)
    ledgers = [l for l in ledgers if not (l['id'] == account_id and l['user_id'] == user_id)]
    if len(ledgers) < initial_count:
        _write_ledgers_to_json(ledgers)
        return True
    return False
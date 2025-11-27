import firebase_config
from datetime import datetime
import uuid

def add_ledger_account(user_id, account_name):
    """Adds a new empty ledger account to the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")
    
    # Check if an account with the same name already exists for this user
    existing_accounts = get_all_ledger_accounts(user_id)
    if any(acc['account_name'] == account_name for acc in existing_accounts):
        return False
        
    account_id = str(uuid.uuid4())
    new_account = {
        'id': account_id,
        'user_id': user_id,
        'account_name': account_name,
        'entries': []
    }
    
    firebase_config.db.child("ledgers").child(user_id).child(account_id).set(new_account)
    return True

def get_all_ledger_accounts(user_id):
    """Retrieves all ledger accounts for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return []
        
    accounts_ref = firebase_config.db.child("ledgers").child(user_id).get()
    if accounts_ref.val():
        return [item.val() for item in accounts_ref.each()]
    return []

def get_ledger_account_by_id(user_id, account_id):
    """Retrieves a single ledger account by its ID for a user."""
    if not firebase_config.db:
        return None
        
    account_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).get()
    return account_ref.val() if account_ref.val() else None

def get_ledger_account_by_name(user_id, account_name):
    """Retrieves a single ledger account by its name for a user."""
    accounts = get_all_ledger_accounts(user_id)
    for account in accounts:
        if account['account_name'] == account_name:
            return account
    return None

def add_entry_to_ledger_account(user_id, account_id, transaction_name, description, transaction_type, billing_number, amount, payment_method):
    """Adds a new entry to a specific ledger account."""
    if not firebase_config.db:
        return False

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
    
    # Get current entries, append the new one, and set it back
    entries_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries")
    entries = entries_ref.get().val() or []
    entries.append(new_entry)
    entries_ref.set(entries)
    return True

def delete_entry_from_ledger_account(user_id, account_id, entry_index):
    """Deletes an entry from a specific ledger account by its index."""
    if not firebase_config.db:
        return False
        
    entries_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries")
    entries = entries_ref.get().val()
    if entries and 0 <= entry_index < len(entries):
        del entries[entry_index]
        entries_ref.set(entries)
        return True
    return False

def mark_ledger_entry_paid(user_id, account_id, entry_index, paid_status):
    """Marks a ledger entry as paid or unpaid."""
    if not firebase_config.db:
        return False
        
    entry_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries").child(str(entry_index)).child("paid")
    entry_ref.set(paid_status)
    return True

def delete_ledger_account(user_id, account_id):
    """Deletes a ledger account by its ID."""
    if not firebase_config.db:
        return False
        
    firebase_config.db.child("ledgers").child(user_id).child(account_id).remove()
    return True

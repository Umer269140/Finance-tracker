import firebase_config
from datetime import datetime
import uuid

def add_ledger_account(session_state, user_id, id_token, is_admin, account_name):
    """Adds a new empty ledger account to the Firebase Realtime Database."""
    if not firebase_config.db:
        raise Exception("Firebase Realtime Database not configured.")
    
    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")

    existing_accounts = get_all_ledger_accounts(session_state, user_id, id_token, is_admin) # Ensure this calls Firebase version
    if any(acc['account_name'] == account_name for acc in existing_accounts):
        return False
        
    account_id = str(uuid.uuid4())
    new_account = {
        'account_name': account_name,
        'entries': []
    }
    
    firebase_config.db.child("ledgers").child(user_id).child(account_id).set(new_account, token=id_token)
    return True

def get_all_ledger_accounts(session_state, user_id, id_token, is_admin):
    """Retrieves all ledger accounts for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return []
    
    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        # If token refresh fails, assume not logged in or session expired
        return []
    try:
        accounts_ref = firebase_config.db.child("ledgers").child(user_id).get(token=id_token)
        if accounts_ref.val():
            accounts = []
            for item in accounts_ref.each():
                account = item.val()
                account['id'] = item.key() # Add the ID from the Firebase key
                accounts.append(account)
            return accounts
        return []
    except Exception as e:
        print(f"Could not get ledger accounts: {e}")
        return []

def get_ledger_account_by_id(session_state, user_id, id_token, is_admin, account_id):
    """Retrieves a single ledger account by its ID for a user from the Firebase Realtime Database."""
    if not firebase_config.db:
        return None

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        # If token refresh fails, assume not logged in or session expired
        return None
        
    account_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).get(token=id_token)
    return account_ref.val() if account_ref.val() else None

def get_ledger_account_by_name(session_state, user_id, id_token, is_admin, account_name):
    """Retrieves a single ledger account by its name for a user from the Firebase Realtime Database."""
    accounts = get_all_ledger_accounts(session_state, user_id, id_token, is_admin) # Pass session_state
    for account in accounts:
        if account['account_name'] == account_name:
            return account
    return None

def add_entry_to_ledger_account(session_state, user_id, id_token, is_admin, account_id, transaction_name, description, transaction_type, billing_number, amount, payment_method):
    """Adds a new entry to a specific ledger account in the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")

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
    
    entries_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries")
    entries = entries_ref.get(token=id_token).val() or []
    entries.append(new_entry)
    entries_ref.set(entries, token=id_token)
    return True

def delete_entry_from_ledger_account(session_state, user_id, id_token, is_admin, account_id, entry_index):
    """Deletes an entry from a specific ledger account by its index in the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")
        
    entries_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries")
    entries = entries_ref.get(token=id_token).val()
    if entries and 0 <= entry_index < len(entries):
        del entries[entry_index]
        entries_ref.set(entries, token=id_token)
        return True
    return False

def mark_ledger_entry_paid(session_state, user_id, id_token, is_admin, account_id, entry_index, paid_status):
    """Marks a ledger entry as paid or unpaid in the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")
        
    entry_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries").child(str(entry_index)).child("paid")
    entry_ref.set(paid_status, token=id_token)
    return True

def delete_ledger_account(session_state, user_id, id_token, is_admin, account_id):
    """Deletes a ledger account by its ID from the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")
        
    firebase_config.db.child("ledgers").child(user_id).child(account_id).remove(token=id_token)
    return True

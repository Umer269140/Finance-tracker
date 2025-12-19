import firebase_config
from datetime import datetime
import uuid

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
                if 'entries' in account and isinstance(account['entries'], dict):
                    # Convert entries dictionary to a list of dictionaries, including the entry ID
                    entries_list = []
                    for entry_id, entry_data in account['entries'].items():
                        entry_data['id'] = entry_id
                        entries_list.append(entry_data)
                    account['entries'] = entries_list
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
    account = account_ref.val()
    if account:
        account['id'] = account_id # Add the ID from the Firebase key
        if 'entries' in account and isinstance(account['entries'], dict):
            # Convert entries dictionary to a list of dictionaries, including the entry ID
            entries_list = []
            for entry_id, entry_data in account['entries'].items():
                entry_data['id'] = entry_id
                entries_list.append(entry_data)
            account['entries'] = entries_list
    return account if account else None

def get_ledger_account_by_name(session_state, user_id, id_token, is_admin, account_name):
    """Retrieves a single ledger account by its name for a user from the Firebase Realtime Database."""
    accounts = get_all_ledger_accounts(session_state, user_id, id_token, is_admin) # Pass session_state
    for account in accounts:
        if account['account_name'] == account_name:
            return account
    return None

def add_entry_to_ledger_account(session_state, user_id, id_token, is_admin, account_id, transaction_name, description, transaction_type, billing_number, amount, payment_method, date):
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
        "date": date,
        "paid": False,
        "payment_method": payment_method
    }
    
    firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries").push(new_entry, token=id_token)
    return True

def delete_entry_from_ledger_account(session_state, user_id, id_token, is_admin, account_id, entry_id):
    """Deletes an entry from a specific ledger account by its ID in the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")
        
    firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries").child(entry_id).remove(token=id_token)
    return True

def mark_ledger_entry_paid(session_state, user_id, id_token, is_admin, account_id, entry_id, paid_status):
    """Marks a ledger entry as paid or unpaid in the Firebase Realtime Database."""
    if not firebase_config.db:
        return False

    # Get a fresh ID token
    id_token = firebase_config.get_fresh_id_token(session_state)
    if not id_token:
        raise Exception("Failed to get a fresh ID token. Please log in again.")
        
    entry_ref = firebase_config.db.child("ledgers").child(user_id).child(account_id).child("entries").child(entry_id).child("paid")
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

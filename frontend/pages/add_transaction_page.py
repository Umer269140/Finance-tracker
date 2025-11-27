import streamlit as st
from datetime import datetime
from features.transactions import transactions as t
from features.ledger import ledger as l

def app():
    st.header("Add a New Transaction")

    transaction_type = st.selectbox("Select transaction type:", ["Expense", "Income"])
    name = st.text_input("Enter name:")
    amount = st.number_input("Enter amount:", min_value=0.0)
    date = st.date_input("Select date:", datetime.today())
    payment_method = st.selectbox("Payment Method:", ["Cash", "Bank Account", "Cheque"]) # New dropdown
    description = st.text_input("Description (optional):")
    billing_number = st.text_input("Billing Number (optional):")

    if st.button("Add Transaction"):
        if name and amount > 0:
            user_id = st.session_state.user_id
            id_token = st.session_state.id_token
            t.add_transaction(user_id, id_token, transaction_type, amount, date.strftime("%Y-%m-%d"), name, description, billing_number, payment_method) # Pass payment_method
            st.success("Transaction added successfully!")

            # Automatically create/add to ledger account with transaction name
            if l.add_ledger_account(user_id, id_token, name): # Try to create a new ledger account
                st.info(f"Ledger account '{name}' created automatically.")
            
            # Get the ledger account (either newly created or existing)
            ledger_account = l.get_ledger_account_by_name(user_id, id_token, name)
            if ledger_account:
                # Add the transaction as an entry to this ledger account
                if l.add_entry_to_ledger_account(
                    user_id,
                    id_token,
                    ledger_account["id"], 
                    name, # Use transaction name as entry name
                    description, # Use user-provided description
                    transaction_type, 
                    billing_number, # Use user-provided billing number
                    amount,
                    payment_method # Pass payment_method to ledger entry
                ):
                    st.success(f"Transaction added as entry to ledger account '{name}'.")
                else:
                    st.error(f"Failed to add transaction as entry to ledger account '{name}'.")
            else:
                st.error(f"Ledger account '{name}' not found after creation attempt.")
            
            st.rerun() # Rerun to clear inputs and update lists
        else:
            st.error("Please fill in all required fields (Name, Amount).")
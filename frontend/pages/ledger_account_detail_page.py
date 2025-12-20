import streamlit as st
from datetime import datetime # Added for date input default
from features.ledger import ledger as l
from features.transactions import transactions as t # Added for adding transactions

def app():
    print("DEBUG: Entering ledger_account_detail_page.app()") # NEW PRINT
    st.header("Ledger Account Details")

    user_id = st.session_state.user_id
    id_token = st.session_state.id_token
    is_admin = st.session_state.get('is_admin', False)

    if 'selected_account_id' in st.session_state and st.session_state.selected_account_id:
        account_id = st.session_state.selected_account_id
        print(f"DEBUG: ledger_account_detail_page - Selected account ID: {account_id}") # NEW PRINT
        account = l.get_ledger_account_by_id(st.session_state, user_id, id_token, is_admin, account_id) # Pass session_state
        print(f"DEBUG: ledger_account_detail_page - Account object after retrieval: {account}") # NEW PRINT

        if account:
            st.subheader(f"Account: {account.get('account_name', 'N/A')}")
            
            entries = account.get("entries", [])
            print(f"DEBUG: ledger_account_detail_page - Entries retrieved from account: {entries}")
            if entries:
                st.write("### Entries:")
                st.markdown("---")
                
                # Header row for entries
                col_name_h, col_desc_h, col_type_h, col_amount_h, col_bill_h, col_date_h, col_del_h = st.columns([1.5, 2, 1, 1, 1.5, 1.5, 0.5])
                with col_name_h:
                    st.write("**Name**")
                with col_desc_h:
                    st.write("**Description**")
                with col_type_h:
                    st.write("**Type**")
                with col_amount_h:
                    st.write("**Amount**")
                with col_bill_h:
                    st.write("**Billing No.**")
                with col_date_h:
                    st.write("**Date**")
                with col_del_h:
                    st.write("**Del**")

                for entry in entries:
                    if isinstance(entry, dict):
                        col_name, col_desc, col_type, col_amount, col_bill, col_date, col_del = st.columns([1.5, 2, 1, 1, 1.5, 1.5, 0.5])
                        with col_name:
                            st.write(entry.get('name', ''))
                        with col_desc:
                            st.write(entry.get('description', ''))
                        with col_type:
                            st.write(entry.get('type', ''))
                        with col_amount:
                            st.write(f"Rs {entry.get('amount', 0.0):.2f}")
                        with col_bill:
                            st.write(entry.get('billing_number', ''))
                        with col_date:
                            st.write(entry.get('date', ''))
                        with col_del:
                            if st.button("X", key=f"delete_entry_{account_id}_{entry.get('id')}"):
                                l.delete_entry_from_ledger_account(st.session_state, user_id, id_token, is_admin, account_id, entry.get('id')) # Pass session_state
                                st.rerun()
                st.markdown("---")
                st.markdown("---")
            else:
                st.write("No entries in this ledger account yet.")

            with st.expander("Add New Entry"):
                with st.form(key='add_entry_form', clear_on_submit=True):
                    entry_name = st.text_input("Entry Name")
                    entry_description = st.text_area("Description")
                    entry_type = st.selectbox("Type", ["Expense", "Income"])
                    entry_amount = st.number_input("Amount", min_value=0.01, step=0.01)
                    entry_billing_number = st.text_input("Billing Number")
                    entry_payment_method = st.selectbox("Payment Method", ["Cash", "Bank Account", "Other"])
                    entry_date = st.date_input("Date", value=datetime.now())
                    submit_button = st.form_submit_button(label='Add Entry')

                    if submit_button:
                        if all([entry_name, entry_description, entry_type, entry_amount, entry_billing_number, entry_payment_method, entry_date]):
                            l.add_entry_to_ledger_account(
                                st.session_state, user_id, id_token, is_admin, account_id,
                                entry_name, entry_description, entry_type, entry_billing_number,
                                entry_amount, entry_payment_method, str(entry_date)
                            )
                            st.success("Entry added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill out all fields.")
            
            if st.button("Back to Ledger Accounts"):
                st.session_state.page = "Ledger"
                st.session_state.selected_account_id = None # Clear selected ID
        else:
            st.error("Ledger account not found.")
            if st.button("Back to Ledger Accounts"):
                st.session_state.page = "Ledger"
                st.session_state.selected_account_id = None # Clear selected ID
    else:
        st.warning("No ledger account selected. Please go back to Ledger Accounts list.")
        if st.button("Back to Ledger Accounts"):
            st.session_state.page = "Ledger"
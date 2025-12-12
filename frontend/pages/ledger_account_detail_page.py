import streamlit as st
from features.ledger import ledger as l

def app():
    st.header("Ledger Account Details")

    user_id = st.session_state.user_id
    id_token = st.session_state.id_token
    is_admin = st.session_state.get('is_admin', False)

    if 'selected_account_id' in st.session_state and st.session_state.selected_account_id:
        account_id = st.session_state.selected_account_id
        account = l.get_ledger_account_by_id(st.session_state, user_id, id_token, is_admin, account_id) # Pass session_state

        if account:
            st.subheader(f"Account: {account.get('account_name', 'N/A')}")
            
            entries = account.get("entries", [])
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
            else:
                st.write("No entries in this ledger account yet.")
            
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
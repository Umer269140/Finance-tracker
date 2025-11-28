import streamlit as st
from features.ledger import ledger as l

def app():
    st.header("Ledger Accounts")
    user_id = st.session_state.user_id
    id_token = st.session_state.id_token
    is_admin = st.session_state.get('is_admin', False)
    accounts = l.get_all_ledger_accounts(user_id, id_token, is_admin)

    # Option to create a new ledger account
    with st.expander("Create New Ledger Account"):
        new_account_name = st.text_input("Enter new ledger account name:")
        if st.button("Create Account"):
            if new_account_name:
                if l.add_ledger_account(user_id, id_token, is_admin, new_account_name):
                    st.success(f"Ledger account '{new_account_name}' created.")
                    st.rerun()
                else:
                    st.error(f"Ledger account '{new_account_name}' already exists.")
            else:
                st.error("Please enter a name for the new ledger account.")

    st.markdown("---")

    if accounts:
        st.write("### Click an account to view its entries:")
        
        # Header row for the list of accounts
        col_name_h, col_delete_h = st.columns([1, 0.2])
        with col_name_h:
            st.write("**Account Name**")
        with col_delete_h:
            st.write("**Del**")

        for account in accounts:
            col_name, col_delete = st.columns([1, 0.2])
            with col_name:
                if st.button(account.get('account_name', 'No Name'), key=f"account_select_{account.get('id')}"):
                    st.session_state.selected_account_id = account.get('id')
                    st.session_state.page = "Ledger Account Detail"
            with col_delete:
                if st.button("X", key=f"delete_account_{account.get('id')}"):
                    l.delete_ledger_account(user_id, id_token, is_admin, account.get('id'))
                    st.rerun()
        st.markdown("---")
    else:
        st.write("No ledger accounts yet. Create one above!")
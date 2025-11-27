import streamlit as st
from features.transactions import transactions as t

def app():
    st.header("All Transactions")
    
    user_id = st.session_state.user_id
    transactions = t.get_all_transactions(user_id)

    if transactions:
        st.write("### Your Transactions")
        st.markdown("---")
        # Header row
        col_date_h, col_type_h, col_name_h, col_amount_h, col_delete_h = st.columns([1, 0.8, 2.5, 1, 0.5])
        with col_date_h:
            st.write("**Date**")
        with col_type_h:
            st.write("**Type**")
        with col_name_h:
            st.write("**Name**")
        with col_amount_h:
            st.write("**Amount**")
        with col_delete_h:
            st.write("**Del**")
        
        for i, trans in enumerate(transactions):
            col_date, col_type, col_name, col_amount, col_delete = st.columns([1, 0.8, 2.5, 1, 0.5])
            with col_date:
                st.write(trans['date'])
            with col_type:
                st.write(trans['type'])
            with col_name:
                st.write(trans.get('name', '')) # Display name
            with col_amount:
                st.write(f"{trans['amount']:.2f}")
            with col_delete:
                delete_button = st.button("X", key=f"delete_trans_{i}")
                if delete_button:
                    t.delete_transaction(user_id, trans['id'])
                    st.rerun()
        st.markdown("---")
    else:
        st.write("No transactions yet.")

    st.subheader("Financial Summary")
    summary = t.get_financial_summary(user_id)
    st.write(f"Total Income: :green[Rs {summary['total_income']:.2f}]")
    st.write(f"Total Expenses: :red[Rs {summary['total_expenses']:.2f}]")
    st.write(f"Current Balance: :blue[Rs {summary['current_balance']:.2f}]")
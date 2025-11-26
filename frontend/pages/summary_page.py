import streamlit as st
from features.transactions import transactions as t

def app():
    st.header("Financial Summary")
    
    user_id = st.session_state.user_id
    summary = t.get_financial_summary(user_id)
    
    st.write(f"Total Income: :green[Rs {summary['total_income']:.2f}]")
    st.write(f"Total Expenses: :red[Rs {summary['total_expenses']:.2f}]")
    st.write(f"Current Balance: :blue[Rs {summary['current_balance']:.2f}]")
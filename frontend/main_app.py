import firebase_config # Initialize Firebase app
import streamlit as st
from pages import add_transaction_page, transactions_list_page, budget_page, summary_page, ledger_page, ledger_account_detail_page, login_page
from features.transactions import transactions as t
from features.ledger import ledger as l

if firebase_config.FIREBASE_INIT_ERROR:
    st.error(f"Firebase Initialization Error: {firebase_config.FIREBASE_INIT_ERROR}")

st.set_page_config(
    page_title="Cashbook Khata",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for white background and black text
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col2:
    st.title("Cashbook Khata")

st.write("Welcome to Cashbook Khata, your personal finance tracker!")
st.subheader("Now the account is easy! cause Its online")

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'id_token' not in st.session_state:
    st.session_state.id_token = None # Initialize id_token to None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False # Initialize is_admin to False

if not st.session_state.logged_in:
    login_page.app()
else:
    # Sidebar for navigation
    st.sidebar.title("Navigation")

    if 'page' not in st.session_state:
        st.session_state.page = "Add Transaction"

    if st.sidebar.button("Add Transaction"):
        st.session_state.page = "Add Transaction"
    if st.sidebar.button("Transactions List"):
        st.session_state.page = "Transactions List"
    if st.sidebar.button("Budget"):
        st.session_state.page = "Budget"
    if st.sidebar.button("Summary"):
        st.session_state.page = "Summary"
    if st.sidebar.button("Ledger"):
        st.session_state.page = "Ledger"

    # Display selected page
    if st.session_state.page == "Add Transaction":
        add_transaction_page.app()
    elif st.session_state.page == "Transactions List":
        transactions_list_page.app()
    elif st.session_state.page == "Budget":
        budget_page.app()
    elif st.session_state.page == "Summary":
        summary_page.app()
    elif st.session_state.page == "Ledger":
        ledger_page.app()
    elif st.session_state.page == "Ledger Account Detail":
        ledger_account_detail_page.app()

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
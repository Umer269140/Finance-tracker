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
    initial_sidebar_state="collapsed", # Changed to collapsed to hide default sidebar
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
    /* Style for the hamburger menu button */
    .hamburger-menu {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
    }
    .stButton>button {
        background-color: #f0f2f6; /* Light gray background */
        color: black;
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

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
    # Header with title and hamburger menu
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    with col2:
        st.title("Cashbook Khata")
    with col3:
        # Hamburger menu button
        if st.button("☰ Menu", key="hamburger_menu"):
            st.session_state.menu_open = not st.session_state.get('menu_open', False)

    st.write("Welcome to Cashbook Khata, your personal finance tracker!")
    st.subheader("Now the account is easy! cause Its online")

    # Display menu options if menu is open
    if st.session_state.get('menu_open', False):
        menu_options = ["Add Transaction", "Transactions List", "Budget", "Summary", "Ledger"]
        selected_option = st.selectbox("Navigate:", menu_options, key="menu_selectbox")
        
        if selected_option:
            st.session_state.page = selected_option
            st.session_state.menu_open = False # Close menu after selection
            st.rerun() # Rerun to navigate

    # Display selected page
    if 'page' not in st.session_state:
        st.session_state.page = "Add Transaction"

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

    st.markdown("---")
    # Logout button at the bottom of the main content area
    if st.button("Logout", key="main_logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user_id = None
        st.session_state.id_token = None
        st.rerun()
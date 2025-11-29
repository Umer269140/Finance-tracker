import streamlit as st
import firebase_config
from firebase_admin import auth as admin_auth
import json
from requests.exceptions import HTTPError

# Admin Credentials
ADMIN_EMAIL = "umerjunaidzakaria@gmail.com"
ADMIN_PASSWORD = "Pagalsimon123"

# Map Firebase error messages to user-friendly messages
FIREBASE_ERROR_MESSAGES = {
    "EMAIL_NOT_FOUND": "Invalid email or password.",
    "INVALID_PASSWORD": "Invalid email or password.",
    "USER_DISABLED": "This account has been disabled.",
    "EMAIL_EXISTS": "This email address is already in use.",
    "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many failed login attempts. Please try again later.",
    "WEAK_PASSWORD : Password should be at least 6 characters": "Password should be at least 6 characters.",
    # Add more as needed
}

def app():
    st.title("Welcome to Cashbook Khata")

    choice = st.selectbox("Login/Signup", ["Login", "Sign up"])

    if choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Check for admin login first
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.session_state.user_id = "admin"  # Fixed user_id for admin
                st.session_state.id_token = None # No Firebase ID token for admin
                st.session_state.page = "Add Transaction"
                st.rerun()
            elif firebase_config.auth:
                try:
                    user = firebase_config.auth.sign_in_with_email_and_password(email, password)
                    st.session_state.logged_in = True
                    st.session_state.is_admin = False # Not an admin user
                    st.session_state.user_id = user['localId']
                    st.session_state.id_token = user['idToken']
                    st.session_state.page = "Add Transaction"
                    st.rerun()
                except HTTPError as e:
                    error_json = json.loads(e.args[1])
                    error_message = error_json.get('error', {}).get('message', 'Authentication failed.')
                    user_friendly_message = FIREBASE_ERROR_MESSAGES.get(error_message, 'Authentication failed. Please check your credentials.')
                    st.error(user_friendly_message)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.error("Firebase is not configured.")

    else: # Sign up
        st.subheader("Create a new account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign up"):
            if firebase_config.auth:
                try:
                    user = firebase_config.auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully! Please login.")
                except HTTPError as e:
                    error_json = json.loads(e.args[1])
                    error_message = error_json.get('error', {}).get('message', 'Account creation failed.')
                    user_friendly_message = FIREBASE_ERROR_MESSAGES.get(error_message, 'Account creation failed. Please try again.')
                    st.error(user_friendly_message)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.error("Firebase is not configured.")
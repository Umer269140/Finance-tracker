import streamlit as st
import firebase_config
from firebase_admin import auth as admin_auth

def app():
    st.title("Welcome to Cashbook Khata")

    choice = st.selectbox("Login/Signup", ["Login", "Sign up"])

    if choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if firebase_config.auth:
                try:
                    user = firebase_config.auth.sign_in_with_email_and_password(email, password)
                    st.session_state.logged_in = True
                    st.session_state.user_id = user['localId']
                    st.session_state.id_token = user['idToken']
                    st.session_state.page = "Add Transaction"
                    st.rerun()
                except Exception as e:
                    st.error(f"Authentication failed: {e}")
            else:
                st.error("Firebase is not configured.")

    else:
        st.subheader("Create a new account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign up"):
            if firebase_config.auth:
                try:
                    user = firebase_config.auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully! Please login.")
                except Exception as e:
                    st.error(f"Could not create account: {e}")
            else:
                st.error("Firebase is not configured.")
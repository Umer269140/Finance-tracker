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

                try:

                    user_id = st.session_state.user_id

                    id_token = st.session_state.id_token

                    is_admin = st.session_state.get('is_admin', False)

    

                    print("Attempting to add transaction...")

    

                    t.add_transaction(st.session_state, user_id, id_token, is_admin, transaction_type, amount, date.strftime("%Y-%m-%d"), name, description, billing_number, payment_method)

    

                    print("Transaction successfully added to database.")

    

                    st.success("Transaction added successfully!")

    


                except Exception as e:

                    st.error(f"An unexpected error occurred: {e}")

                    print(f"Caught exception: {e}")

    

            else:

                st.error("Please fill in all required fields (Name, Amount).")

    
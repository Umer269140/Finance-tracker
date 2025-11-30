import streamlit as st
from datetime import datetime
from features.transactions import transactions as t
from features.budgets import budgets as b

st.set_page_config(
    page_title="Cashbook Khata",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to inject for white background and black text
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

st.header("Add a New Transaction")
transaction_type = st.selectbox("Select transaction type:", ["Expense", "Income"])
name = st.text_input("Enter name:")
amount = st.number_input("Enter amount:", min_value=0, step=1)
date = st.date_input("Select date:", datetime.today())

if st.button("Add Transaction"):
    if name and amount > 0:
        t.add_transaction(transaction_type, amount, date, name)
        st.success("Transaction added successfully!")
    else:
        st.error("Please fill in all fields.")

st.header("Set Monthly Budget")
budget_category = st.selectbox("Select category for budget:", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"])
budget_amount = st.number_input("Enter monthly budget amount:", min_value=0, step=1)

if st.button("Set Budget"):
    if budget_category and budget_amount > 0:
        b.set_budget(budget_category, budget_amount)
        st.success(f"Monthly budget of Rs {budget_amount:.2f} set for {budget_category}.")
    else:
        st.error("Please enter a valid category and amount for the budget.")

st.header("Monthly Budget Summary")
transactions_for_budget = t.get_all_transactions() # Get transactions again for budget calculation
budget_summary = b.get_budget_summary(transactions_for_budget)

if budget_summary["budget_details"]:
    budget_table_data = []
    for budget_item in budget_summary["budget_details"]:
        utilization_bar = ""
        if budget_item["utilization_percent"] <= 70:
            utilization_bar = f":green[{budget_item['utilization_percent']:.2f}%]"
        elif budget_item["utilization_percent"] <= 100:
            utilization_bar = f":orange[{budget_item['utilization_percent']:.2f}%]"
        else:
            utilization_bar = f":red[{budget_item['utilization_percent']:.2f}%]"
        
        budget_table_data.append([
            budget_item["category"],
            f"Rs {budget_item['budget_amount']:.2f}",
            f"Rs {budget_item['spent']:.2f}",
            f"Rs {budget_item['remaining']:.2f}",
            utilization_bar,
            budget_item["status"]
        ])
    st.table([["Category", "Budget", "Spent", "Remaining", "Utilization", "Status"]] + budget_table_data)

    st.subheader("Overall Budget Performance")
    st.write(f"Total Monthly Budget: Rs {budget_summary['total_budget_amount']:.2f}")
    st.write(f"Total Spent: Rs {budget_summary['total_spent_amount']:.2f}")
    st.write(f"Total Remaining: Rs {budget_summary['overall_remaining']:.2f}")
    
    overall_utilization_color = "green"
    if budget_summary['overall_utilization_percent'] >= 100:
        overall_utilization_color = "red"
    elif budget_summary['overall_utilization_percent'] >= 70:
        overall_utilization_color = "orange"
    st.markdown(f"Overall Utilization: :{overall_utilization_color}[{budget_summary['overall_utilization_percent']:.2f}%]")

    if budget_summary["categories_over_budget"]:
        st.warning(f"Categories over budget: {', '.join(budget_summary['categories_over_budget'])}")
else:
    st.write("No budgets set yet.")

st.header("All Transactions")
transactions = t.get_all_transactions()

# The order of transactions displayed here directly reflects the order in transactions.txt.
# New transactions are appended, and deletions rewrite the file, preserving relative order.

if transactions:
    # Create a list of lists for the table data
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
        st.write("**Action**")
    
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
            delete_button = st.button("Delete", key=f"delete_{i}")
            if delete_button:
                t.delete_transaction(i)
                st.rerun()
    st.markdown("---")
else:
    st.write("No transactions yet.")
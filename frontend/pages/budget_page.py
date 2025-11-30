import streamlit as st
from features.budgets import budgets as b

def app():
    st.header("Set Monthly Budget")
    
    user_id = st.session_state.user_id
    id_token = st.session_state.id_token
    is_admin = st.session_state.get('is_admin', False)
    
    all_categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
    budget_category = st.selectbox("Select category for budget:", all_categories)
    budget_amount = st.number_input("Enter monthly budget amount:", min_value=0.0)

    if st.button("Set Budget"):
        if budget_category and budget_amount > 0:
            b.set_budget(st.session_state, user_id, id_token, is_admin, budget_category, budget_amount) # Pass session_state
            st.success(f"Monthly budget of Rs {budget_amount:.2f} set for {budget_category}.")
            st.rerun()
        else:
            st.error("Please enter a valid category and amount for the budget.")

    st.header("Monthly Budget Summary")
    budget_summary = b.get_budget_summary(st.session_state, user_id, id_token, is_admin) # Pass session_state

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
"""Dashboard page component for the expense tracker"""

from datetime import UTC, datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def show_dashboard(manager, show_success_message, show_error_message):  # noqa: PLR0915
    """Display the main dashboard"""
    st.header("📊 Dashboard")

    # Get statistics
    stats = manager.get_statistics()

    if stats["total_expenses"] == 0:
        st.info("No expenses found. Add some expenses to see your dashboard!")

        # Quick add expense form
        st.subheader("Quick Add Expense")
        with st.form("quick_add_expense"):
            col1, col2 = st.columns(2)

            with col1:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
                description = st.text_input("Description")

            with col2:
                categories = manager.get_available_categories()
                category = st.selectbox("Category", categories)
                date = st.date_input("Date", value=datetime.now(tz=UTC).date())

            if st.form_submit_button("Add Expense", type="primary"):
                if amount and description:
                    success = manager.add_expense(
                        amount=amount,
                        description=description,
                        category=category,
                        date=str(date),
                    )

                    if success:
                        show_success_message(f"Added expense: ${amount:.2f} for {description}")
                        st.rerun()
                    else:
                        show_error_message("Failed to add expense")
                else:
                    show_error_message("Please fill in all required fields")

        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Expenses", value=f"${stats['total_amount']:.2f}", delta=None)

    with col2:
        st.metric(label="Number of Expenses", value=stats["total_expenses"], delta=None)

    with col3:
        st.metric(label="Average Expense", value=f"${stats['average_expense']:.2f}", delta=None)

    with col4:
        st.metric(label="Categories", value=stats["categories_count"], delta=None)

    # Recent expenses and category breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Expenses")
        recent_expenses = manager.get_recent_expenses(5)

        if recent_expenses:
            recent_df = pd.DataFrame(recent_expenses)
            recent_df = recent_df[["date", "description", "category", "amount"]].copy()
            recent_df["amount"] = recent_df["amount"].apply(lambda x: f"${x:.2f}")

            st.dataframe(
                recent_df,
                column_config={
                    "date": "Date",
                    "description": "Description",
                    "category": "Category",
                    "amount": "Amount",
                },
                hide_index=True,
                use_container_width=True,
            )

    with col2:
        st.subheader("Spending by Category")
        category_summary = manager.get_category_summary()

        if category_summary:
            # Create pie chart
            categories = list(category_summary.keys())
            amounts = [category_summary[cat]["total"] for cat in categories]

            fig = px.pie(values=amounts, names=categories, title="Expense Distribution by Category")
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

    # Monthly trend
    st.subheader("Monthly Spending Trend")
    monthly_summary = manager.get_monthly_summary()

    if not monthly_summary.empty:
        # Create line chart for monthly totals
        monthly_totals = monthly_summary["Total"].reset_index()
        monthly_totals.columns = ["Month", "Total"]

        fig = px.line(monthly_totals, x="Month", y="Total", title="Monthly Spending Trend", markers=True)
        fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
        st.plotly_chart(fig, use_container_width=True)

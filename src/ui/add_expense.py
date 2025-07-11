"""Add expense page component for the expense tracker"""

from datetime import UTC, datetime

import streamlit as st


def show_add_expense(manager, show_success_message, show_error_message):
    """Display the add expense page"""
    st.header("➕ Add New Expense")  # noqa: RUF001

    with st.form("add_expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, help="Enter the expense amount")

            description = st.text_input("Description", help="Brief description of the expense")

        with col2:
            categories = manager.get_available_categories()
            category = st.selectbox("Category", categories, help="Select or type a category")

            # Option to add custom category
            custom_category = st.text_input("Or enter new category", help="Leave empty to use selected category above")

            date = st.date_input("Date", value=datetime.now(tz=UTC).date(), help="Date of the expense")

        # Submit button
        submitted = st.form_submit_button("Add Expense", type="primary")

        if submitted:
            if amount and description:
                # Use custom category if provided
                final_category = custom_category.strip() if custom_category.strip() else category

                success = manager.add_expense(
                    amount=amount,
                    description=description,
                    category=final_category,
                    date=str(date),
                )

                if success:
                    show_success_message(f"Successfully added expense: ${amount:.2f} for {description}")
                    st.rerun()
                else:
                    show_error_message("Failed to add expense. Please try again.")
            else:
                show_error_message("Please fill in all required fields (Amount and Description)")

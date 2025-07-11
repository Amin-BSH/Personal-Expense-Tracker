"""View expenses page component for the expense tracker"""

from datetime import UTC, datetime

import pandas as pd
import streamlit as st


def show_view_expenses(manager, show_success_message, show_error_message):
    """Display the view expenses page"""
    st.header("👀 View Expenses")

    # Filters
    st.subheader("Filters")
    col1, col2, col3 = st.columns(3)

    with col1:
        # Category filter
        categories = ["All"] + manager.get_available_categories()  # noqa: RUF005
        selected_category = st.selectbox("Filter by Category", categories)

    with col2:
        # Date range filter - Set a wider default range to include sample data
        default_start = datetime(2024, 1, 1).date()  # Start from 2024 to include sample data  # noqa: DTZ001
        default_end = datetime.now(tz=UTC).date()

        date_range = st.date_input(
            "Date Range",
            value=(default_start, default_end),
            help="Select start and end dates",
        )

    with col3:
        # Search
        search_query = st.text_input("Search Description", help="Search in expense descriptions")

    # Get filtered expenses
    if selected_category == "All":
        expenses = manager.get_all_expenses()
    else:
        expenses = manager.get_expenses_by_category(selected_category)

    # Apply date filter
    if len(date_range) == 2:  # noqa: PLR2004
        start_date, end_date = date_range
        expenses = [
            exp
            for exp in expenses
            if start_date <= datetime.strptime(exp["date"], "%Y-%m-%d").date() <= end_date  # noqa: DTZ007
        ]

    # Apply search filter
    if search_query:
        expenses = [exp for exp in expenses if search_query.lower() in exp["description"].lower()]

    # Display results
    if expenses:
        st.subheader(f"Found {len(expenses)} expenses")

        # Convert to DataFrame for display
        df = pd.DataFrame(expenses)  # noqa: PD901
        df = df[["id", "date", "description", "category", "amount"]].copy()  # noqa: PD901
        df = df.sort_values("date", ascending=False)  # noqa: PD901

        # Format amount column
        df["amount"] = df["amount"].apply(lambda x: f"${x:.2f}")

        # Display with edit/delete options
        for idx, expense in df.iterrows():  # noqa: B007
            with st.expander(f"{expense['date']} - {expense['description']} - {expense['amount']}"):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Category:** {expense['category']}")
                    st.write(f"**Amount:** {expense['amount']}")
                    st.write(f"**Description:** {expense['description']}")

                with col2:
                    if st.button("Edit", key=f"edit_{expense['id']}"):
                        st.session_state[f"editing_{expense['id']}"] = True

                with col3:
                    if st.button("Delete", key=f"delete_{expense['id']}", type="secondary"):
                        if manager.delete_expense(expense["id"]):
                            show_success_message(f"Deleted expense: {expense['description']}")
                            st.rerun()
                        else:
                            show_error_message("Failed to delete expense")

                # Edit form
                if st.session_state.get(f"editing_{expense['id']}", False):
                    _show_edit_form(expense, manager, show_success_message, show_error_message)

        # Summary statistics
        _show_summary_statistics(expenses)

    else:
        st.info("No expenses found matching your criteria.")


def _show_edit_form(expense, manager, show_success_message, show_error_message):
    """Display the edit form for an expense"""
    with st.form(f"edit_form_{expense['id']}"):
        st.write("**Edit Expense**")

        # Get original expense data
        original_expense = manager.get_expense_by_id(expense["id"])

        edit_col1, edit_col2 = st.columns(2)

        with edit_col1:
            new_amount = st.number_input(
                "Amount",
                value=float(original_expense["amount"]),
                min_value=0.01,
                step=0.01,
                key=f"edit_amount_{expense['id']}",
            )

            new_description = st.text_input(
                "Description",
                value=original_expense["description"],
                key=f"edit_desc_{expense['id']}",
            )

        with edit_col2:
            categories = manager.get_available_categories()
            current_category_idx = (
                categories.index(original_expense["category"]) if original_expense["category"] in categories else 0
            )

            new_category = st.selectbox(
                "Category",
                categories,
                index=current_category_idx,
                key=f"edit_cat_{expense['id']}",
            )

            new_date = st.date_input(
                "Date",
                value=datetime.strptime(original_expense["date"], "%Y-%m-%d").date(),  # noqa: DTZ007
                key=f"edit_date_{expense['id']}",
            )

        col_save, col_cancel = st.columns(2)

        with col_save:
            if st.form_submit_button("Save Changes", type="primary"):
                success = manager.update_expense(
                    expense["id"],
                    amount=new_amount,
                    description=new_description,
                    category=new_category,
                    date=str(new_date),
                )

                if success:
                    show_success_message("Expense updated successfully")
                    st.session_state[f"editing_{expense['id']}"] = False
                    st.rerun()
                else:
                    show_error_message("Failed to update expense")

        with col_cancel:
            if st.form_submit_button("Cancel"):
                st.session_state[f"editing_{expense['id']}"] = False
                st.rerun()


def _show_summary_statistics(expenses):
    """Display summary statistics for the filtered expenses"""
    st.subheader("Summary")

    # Ensure we're working with numeric amounts only
    valid_amounts = []
    for exp in expenses:
        try:
            amount = float(exp["amount"])
            valid_amounts.append(amount)
        except (ValueError, TypeError):
            # Skip invalid amounts
            continue

    total_amount = sum(valid_amounts)
    avg_amount = total_amount / len(valid_amounts) if valid_amounts else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Amount", f"${total_amount:.2f}")
    with col2:
        st.metric("Average Amount", f"${avg_amount:.2f}")
    with col3:
        st.metric("Number of Expenses", len(expenses))

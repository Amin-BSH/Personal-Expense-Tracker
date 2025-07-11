"""Personal Expense Tracker with Streamlit GUI
A comprehensive expense management application with data visualization and analytics
"""

import sys
from pathlib import Path

import streamlit as st

from src.ui.add_expense import show_add_expense
from src.ui.analytics import show_analytics
from src.ui.dashboard import show_dashboard
from src.ui.manage_data import show_manage_data
from src.ui.view_expenses import show_view_expenses

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).resolve().parent))

from expense_manager import ExpenseManager

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "expense_manager" not in st.session_state:
    st.session_state.expense_manager = ExpenseManager()

if "show_success" not in st.session_state:
    st.session_state.show_success = False

if "success_message" not in st.session_state:
    st.session_state.success_message = ""


def show_success_message(message):
    """Display success message"""
    st.session_state.show_success = True
    st.session_state.success_message = message


def show_error_message(message):
    """Display error message"""
    st.error(message)


def main():
    """Main application function"""

    # Header
    st.markdown('<h1 class="main-header">💰 Personal Expense Tracker</h1>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Add Expense", "View Expenses", "Analytics", "Manage Data"],
    )

    # Add some spacing before footer
    st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True)

    # Footer section
    st.sidebar.markdown("---")
    st.sidebar.markdown("💰 **Personal Expense Tracker**")
    st.sidebar.markdown("Built with Streamlit")

    # Display success message if exists
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False

    # Route to different pages
    manager = st.session_state.expense_manager
    if page == "Dashboard":
        # manager = st.session_state.expense_manager
        show_dashboard(
            manager=manager,
            show_error_message=show_error_message,
            show_success_message=show_success_message,
        )
    elif page == "Add Expense":
        # manager = st.session_state.expense_manager
        show_add_expense(
            manager=manager,
            show_error_message=show_error_message,
            show_success_message=show_success_message,
        )
    elif page == "View Expenses":
        # manager = st.session_state.expense_manager
        show_view_expenses(
            manager=manager,
            show_error_message=show_error_message,
            show_success_message=show_success_message,
        )
    elif page == "Analytics":
        # manager = st.session_state.expense_manager
        show_analytics(
            manager=manager,
        )
    elif page == "Manage Data":
        # manager = st.session_state.expense_manager
        show_manage_data(
            manager=manager,
            show_error_message=show_error_message,
            show_success_message=show_success_message,
        )


# def show_dashboard():
#     """Display the main dashboard"""
#     st.header("📊 Dashboard")

#     manager = st.session_state.expense_manager

#     # Get statistics
#     stats = manager.get_statistics()

#     if stats["total_expenses"] == 0:
#         st.info("No expenses found. Add some expenses to see your dashboard!")

#         # Quick add expense form
#         st.subheader("Quick Add Expense")
#         with st.form("quick_add_expense"):
#             col1, col2 = st.columns(2)

#             with col1:
#                 amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
#                 description = st.text_input("Description")

#             with col2:
#                 categories = manager.get_available_categories()
#                 category = st.selectbox("Category", categories)
#                 date = st.date_input("Date", value=datetime.now().date())

#             if st.form_submit_button("Add Expense", type="primary"):
#                 if amount and description:
#                     success = manager.add_expense(
#                         amount=amount, description=description, category=category, date=str(date)
#                     )

#                     if success:
#                         show_success_message(f"Added expense: ${amount:.2f} for {description}")
#                         st.rerun()
#                     else:
#                         show_error_message("Failed to add expense")
#                 else:
#                     show_error_message("Please fill in all required fields")

#         return

#     # Key metrics
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(label="Total Expenses", value=f"${stats['total_amount']:.2f}", delta=None)

#     with col2:
#         st.metric(label="Number of Expenses", value=stats["total_expenses"], delta=None)

#     with col3:
#         st.metric(label="Average Expense", value=f"${stats['average_expense']:.2f}", delta=None)

#     with col4:
#         st.metric(label="Categories", value=stats["categories_count"], delta=None)

#     # Recent expenses and category breakdown
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Recent Expenses")
#         recent_expenses = manager.get_recent_expenses(5)

#         if recent_expenses:
#             recent_df = pd.DataFrame(recent_expenses)
#             recent_df = recent_df[["date", "description", "category", "amount"]].copy()
#             recent_df["amount"] = recent_df["amount"].apply(lambda x: f"${x:.2f}")

#             st.dataframe(
#                 recent_df,
#                 column_config={
#                     "date": "Date",
#                     "description": "Description",
#                     "category": "Category",
#                     "amount": "Amount",
#                 },
#                 hide_index=True,
#                 use_container_width=True,
#             )

#     with col2:
#         st.subheader("Spending by Category")
#         category_summary = manager.get_category_summary()

#         if category_summary:
#             # Create pie chart
#             categories = list(category_summary.keys())
#             amounts = [category_summary[cat]["total"] for cat in categories]

#             fig = px.pie(values=amounts, names=categories, title="Expense Distribution by Category")
#             fig.update_traces(textposition="inside", textinfo="percent+label")
#             st.plotly_chart(fig, use_container_width=True)

#     # Monthly trend
#     st.subheader("Monthly Spending Trend")
#     monthly_summary = manager.get_monthly_summary()

#     if not monthly_summary.empty:
#         # Create line chart for monthly totals
#         monthly_totals = monthly_summary["Total"].reset_index()
#         monthly_totals.columns = ["Month", "Total"]

#         fig = px.line(monthly_totals, x="Month", y="Total", title="Monthly Spending Trend", markers=True)
#         fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
#         st.plotly_chart(fig, use_container_width=True)


# def show_add_expense():
#     """Display the add expense page"""
#     st.header("➕ Add New Expense")

#     manager = st.session_state.expense_manager

#     with st.form("add_expense_form"):
#         col1, col2 = st.columns(2)

#         with col1:
#             amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, help="Enter the expense amount")

#             description = st.text_input("Description", help="Brief description of the expense")

#         with col2:
#             categories = manager.get_available_categories()
#             category = st.selectbox("Category", categories, help="Select or type a category")

#             # Option to add custom category
#             custom_category = st.text_input("Or enter new category", help="Leave empty to use selected category above")

#             date = st.date_input("Date", value=datetime.now().date(), help="Date of the expense")

#         # Submit button
#         submitted = st.form_submit_button("Add Expense", type="primary")

#         if submitted:
#             if amount and description:
#                 # Use custom category if provided
#                 final_category = custom_category.strip() if custom_category.strip() else category

#                 success = manager.add_expense(
#                     amount=amount, description=description, category=final_category, date=str(date)
#                 )

#                 if success:
#                     show_success_message(f"Successfully added expense: ${amount:.2f} for {description}")
#                     st.rerun()
#                 else:
#                     show_error_message("Failed to add expense. Please try again.")
#             else:
#                 show_error_message("Please fill in all required fields (Amount and Description)")


# def show_view_expenses():
#     """Display the view expenses page"""
#     st.header("👀 View Expenses")

#     manager = st.session_state.expense_manager

#     # Filters
#     st.subheader("Filters")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         # Category filter
#         categories = ["All"] + manager.get_available_categories()
#         selected_category = st.selectbox("Filter by Category", categories)

#     with col2:
#         # Date range filter - Set a wider default range to include sample data
#         default_start = datetime(2024, 1, 1).date()  # Start from 2024 to include sample data
#         default_end = datetime.now().date()

#         date_range = st.date_input(
#             "Date Range",
#             value=(default_start, default_end),
#             help="Select start and end dates",
#         )

#     with col3:
#         # Search
#         search_query = st.text_input("Search Description", help="Search in expense descriptions")

#     # Get filtered expenses
#     if selected_category == "All":
#         expenses = manager.get_all_expenses()
#     else:
#         expenses = manager.get_expenses_by_category(selected_category)

#     # Apply date filter
#     if len(date_range) == 2:
#         start_date, end_date = date_range
#         expenses = [
#             exp for exp in expenses if start_date <= datetime.strptime(exp["date"], "%Y-%m-%d").date() <= end_date
#         ]

#     # Apply search filter
#     if search_query:
#         expenses = [exp for exp in expenses if search_query.lower() in exp["description"].lower()]

#     # Display results
#     if expenses:
#         st.subheader(f"Found {len(expenses)} expenses")

#         # Convert to DataFrame for display
#         df = pd.DataFrame(expenses)
#         df = df[["id", "date", "description", "category", "amount"]].copy()
#         df = df.sort_values("date", ascending=False)

#         # Format amount column
#         df["amount"] = df["amount"].apply(lambda x: f"${x:.2f}")

#         # Display with edit/delete options
#         for idx, expense in df.iterrows():
#             with st.expander(f"{expense['date']} - {expense['description']} - {expense['amount']}"):
#                 col1, col2, col3 = st.columns([2, 1, 1])

#                 with col1:
#                     st.write(f"**Category:** {expense['category']}")
#                     st.write(f"**Amount:** {expense['amount']}")
#                     st.write(f"**Description:** {expense['description']}")

#                 with col2:
#                     if st.button(f"Edit", key=f"edit_{expense['id']}"):
#                         st.session_state[f"editing_{expense['id']}"] = True

#                 with col3:
#                     if st.button(f"Delete", key=f"delete_{expense['id']}", type="secondary"):
#                         if manager.delete_expense(expense["id"]):
#                             show_success_message(f"Deleted expense: {expense['description']}")
#                             st.rerun()
#                         else:
#                             show_error_message("Failed to delete expense")

#                 # Edit form
#                 if st.session_state.get(f"editing_{expense['id']}", False):
#                     with st.form(f"edit_form_{expense['id']}"):
#                         st.write("**Edit Expense**")

#                         # Get original expense data
#                         original_expense = manager.get_expense_by_id(expense["id"])

#                         edit_col1, edit_col2 = st.columns(2)

#                         with edit_col1:
#                             new_amount = st.number_input(
#                                 "Amount",
#                                 value=float(original_expense["amount"]),
#                                 min_value=0.01,
#                                 step=0.01,
#                                 key=f"edit_amount_{expense['id']}",
#                             )

#                             new_description = st.text_input(
#                                 "Description", value=original_expense["description"], key=f"edit_desc_{expense['id']}"
#                             )

#                         with edit_col2:
#                             categories = manager.get_available_categories()
#                             current_category_idx = (
#                                 categories.index(original_expense["category"])
#                                 if original_expense["category"] in categories
#                                 else 0
#                             )

#                             new_category = st.selectbox(
#                                 "Category", categories, index=current_category_idx, key=f"edit_cat_{expense['id']}"
#                             )

#                             new_date = st.date_input(
#                                 "Date",
#                                 value=datetime.strptime(original_expense["date"], "%Y-%m-%d").date(),
#                                 key=f"edit_date_{expense['id']}",
#                             )

#                         col_save, col_cancel = st.columns(2)

#                         with col_save:
#                             if st.form_submit_button("Save Changes", type="primary"):
#                                 success = manager.update_expense(
#                                     expense["id"],
#                                     amount=new_amount,
#                                     description=new_description,
#                                     category=new_category,
#                                     date=str(new_date),
#                                 )

#                                 if success:
#                                     show_success_message("Expense updated successfully")
#                                     st.session_state[f"editing_{expense['id']}"] = False
#                                     st.rerun()
#                                 else:
#                                     show_error_message("Failed to update expense")

#                         with col_cancel:
#                             if st.form_submit_button("Cancel"):
#                                 st.session_state[f"editing_{expense['id']}"] = False
#                                 st.rerun()

#         # Summary statistics
#         st.subheader("Summary")
#         # Ensure we're working with numeric amounts only
#         valid_amounts = []
#         for exp in expenses:
#             try:
#                 amount = float(exp["amount"])
#                 valid_amounts.append(amount)
#             except (ValueError, TypeError):
#                 # Skip invalid amounts
#                 continue

#         total_amount = sum(valid_amounts)
#         avg_amount = total_amount / len(valid_amounts) if valid_amounts else 0

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Total Amount", f"${total_amount:.2f}")
#         with col2:
#             st.metric("Average Amount", f"${avg_amount:.2f}")
#         with col3:
#             st.metric("Number of Expenses", len(expenses))

#     else:
#         st.info("No expenses found matching your criteria.")


# def show_analytics():
#     """Display the analytics page"""
#     st.header("📈 Analytics & Reports")

#     manager = st.session_state.expense_manager
#     expenses = manager.get_all_expenses()

#     if not expenses:
#         st.info("No expenses found. Add some expenses to see analytics!")
#         return

#     # Convert to DataFrame
#     df = pd.DataFrame(expenses)
#     df["date"] = pd.to_datetime(df["date"])
#     df["month_str"] = df["date"].dt.strftime("%Y-%m")  # Use string format instead of Period
#     df["month_name"] = df["date"].dt.strftime("%B %Y")  # Human readable month
#     df["weekday"] = df["date"].dt.day_name()

#     # Analytics tabs
#     tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Categories", "Patterns"])

#     with tab1:
#         st.subheader("Expense Overview")

#         # Key statistics
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.metric("Total Spent", f"${df['amount'].sum():.2f}")
#         with col2:
#             st.metric("Average Expense", f"${df['amount'].mean():.2f}")
#         with col3:
#             st.metric("Highest Expense", f"${df['amount'].max():.2f}")
#         with col4:
#             st.metric("Lowest Expense", f"${df['amount'].min():.2f}")

#         # Expense distribution
#         col1, col2 = st.columns(2)

#         with col1:
#             # Histogram of expense amounts
#             fig = px.histogram(df, x="amount", nbins=20, title="Distribution of Expense Amounts")
#             fig.update_layout(xaxis_title="Amount ($)", yaxis_title="Frequency")
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             # Box plot by category
#             fig = px.box(df, x="category", y="amount", title="Expense Amount Distribution by Category")
#             fig.update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
#             fig.update_xaxes(tickangle=45)
#             st.plotly_chart(fig, use_container_width=True)

#     with tab2:
#         st.subheader("Spending Trends")

#         # Monthly trend
#         monthly_spending = df.groupby("month_name")["amount"].sum().reset_index()
#         monthly_spending = monthly_spending.sort_values("month_name")  # Sort chronologically

#         fig = px.line(monthly_spending, x="month_name", y="amount", title="Monthly Spending Trend", markers=True)
#         fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
#         fig.update_xaxes(tickangle=45)
#         st.plotly_chart(fig, use_container_width=True)

#         # Daily spending pattern
#         daily_spending = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
#         daily_spending.columns = ["date", "amount"]

#         # Convert date column to datetime for proper plotting
#         daily_spending["date"] = pd.to_datetime(daily_spending["date"])

#         fig = px.scatter(daily_spending, x="date", y="amount", title="Daily Spending Pattern", trendline="lowess")
#         fig.update_layout(xaxis_title="Date", yaxis_title="Amount ($)")
#         st.plotly_chart(fig, use_container_width=True)

#     with tab3:
#         st.subheader("Category Analysis")

#         # Category spending
#         category_spending = df.groupby("category")["amount"].agg(["sum", "count", "mean"]).reset_index()
#         category_spending.columns = ["Category", "Total", "Count", "Average"]
#         category_spending = category_spending.sort_values("Total", ascending=False)

#         col1, col2 = st.columns(2)

#         with col1:
#             # Bar chart of category totals
#             fig = px.bar(category_spending, x="Category", y="Total", title="Total Spending by Category")
#             fig.update_layout(xaxis_title="Category", yaxis_title="Total Amount ($)")
#             fig.update_xaxes(tickangle=45)
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             # Category summary table
#             st.write("**Category Summary**")
#             category_display = category_spending.copy()
#             category_display["Total"] = category_display["Total"].apply(lambda x: f"${x:.2f}")
#             category_display["Average"] = category_display["Average"].apply(lambda x: f"${x:.2f}")

#             st.dataframe(category_display, hide_index=True, use_container_width=True)

#     with tab4:
#         st.subheader("Spending Patterns")

#         # Day of week analysis
#         weekday_spending = df.groupby("weekday")["amount"].agg(["sum", "mean"]).reset_index()

#         # Reorder days
#         day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         weekday_spending["weekday"] = pd.Categorical(weekday_spending["weekday"], categories=day_order, ordered=True)
#         weekday_spending = weekday_spending.sort_values("weekday")

#         col1, col2 = st.columns(2)

#         with col1:
#             fig = px.bar(weekday_spending, x="weekday", y="sum", title="Total Spending by Day of Week")
#             fig.update_layout(xaxis_title="Day of Week", yaxis_title="Total Amount ($)")
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             fig = px.bar(weekday_spending, x="weekday", y="mean", title="Average Spending by Day of Week")
#             fig.update_layout(xaxis_title="Day of Week", yaxis_title="Average Amount ($)")
#             st.plotly_chart(fig, use_container_width=True)

#         # Monthly category heatmap
#         try:
#             # Create monthly category pivot table using string dates
#             monthly_category_data = df.groupby(["month_name", "category"])["amount"].sum().reset_index()
#             monthly_category_pivot = monthly_category_data.pivot(
#                 index="month_name", columns="category", values="amount"
#             ).fillna(0)

#             if not monthly_category_pivot.empty:
#                 # Convert to numpy array for plotly
#                 z_data = monthly_category_pivot.values
#                 x_labels = monthly_category_pivot.columns.tolist()
#                 y_labels = monthly_category_pivot.index.tolist()

#                 fig = px.imshow(
#                     z_data,
#                     x=x_labels,
#                     y=y_labels,
#                     title="Monthly Spending Heatmap by Category",
#                     aspect="auto",
#                     color_continuous_scale="Blues",
#                     labels=dict(x="Category", y="Month", color="Amount ($)"),
#                 )
#                 fig.update_layout(xaxis_title="Category", yaxis_title="Month")
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("Not enough data for heatmap visualization")
#         except Exception as e:
#             st.warning(f"Could not generate heatmap: {str(e)}")
#             st.info("This visualization requires data from multiple months and categories")


# def show_manage_data():
#     """Display the data management page"""
#     st.header("🔧 Manage Data")

#     manager = st.session_state.expense_manager

#     # Data statistics
#     stats = manager.get_statistics()

#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Database Statistics")
#         st.write(f"**Total Expenses:** {stats['total_expenses']}")
#         st.write(f"**Total Amount:** ${stats['total_amount']:.2f}")
#         st.write(f"**Categories:** {stats['categories_count']}")

#         if stats["date_range"]:
#             st.write(f"**Date Range:** {stats['date_range']['start']} to {stats['date_range']['end']}")

#     with col2:
#         st.subheader("Quick Actions")

#         # Import fake data
#         if st.button("Import Sample Data", help="Add 50 sample expenses for testing"):
#             if manager.import_fake_data():
#                 show_success_message("Sample data imported successfully!")
#                 st.rerun()
#             else:
#                 show_error_message("Failed to import sample data")

#         # Export data
#         if st.button("Export to CSV", help="Download all expenses as CSV"):
#             filename = manager.export_to_csv()
#             if filename:
#                 show_success_message(f"Data exported to {filename}")
#             else:
#                 show_error_message("Failed to export data")

#     st.divider()

#     # Dangerous operations
#     st.subheader("⚠️ Dangerous Operations")
#     st.warning("These operations cannot be undone!")

#     # Clear all data
#     if st.button("Clear All Data", type="secondary", help="Delete all expenses permanently"):
#         if st.session_state.get("confirm_clear", False):
#             if manager.clear_all_data():
#                 show_success_message("All data cleared successfully")
#                 st.session_state["confirm_clear"] = False
#                 st.rerun()
#             else:
#                 show_error_message("Failed to clear data")
#         else:
#             st.session_state["confirm_clear"] = True
#             st.error("Click again to confirm deletion of all data")

#     # Reset confirmation state
#     if st.session_state.get("confirm_clear", False):
#         if st.button("Cancel", type="primary"):
#             st.session_state["confirm_clear"] = False
#             st.rerun()


if __name__ == "__main__":
    main()

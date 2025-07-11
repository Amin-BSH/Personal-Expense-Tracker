"""Analytics page component for the expense tracker"""

import pandas as pd
import plotly.express as px
import streamlit as st


def show_analytics(manager):
    """Display the analytics page"""
    st.header("📈 Analytics & Reports")

    expenses = manager.get_all_expenses()

    if not expenses:
        st.info("No expenses found. Add some expenses to see analytics!")
        return

    # Convert to DataFrame
    df = pd.DataFrame(expenses)  # noqa: PD901
    df["date"] = pd.to_datetime(df["date"])
    df["month_str"] = df["date"].dt.strftime("%Y-%m")  # Use string format instead of Period
    df["month_name"] = df["date"].dt.strftime("%B %Y")  # Human readable month
    df["weekday"] = df["date"].dt.day_name()

    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Categories", "Patterns"])

    with tab1:
        _show_overview_tab(df)

    with tab2:
        _show_trends_tab(df)

    with tab3:
        _show_categories_tab(df)

    with tab4:
        _show_patterns_tab(df)


def _show_overview_tab(df):
    """Display the overview analytics tab"""
    st.subheader("Expense Overview")

    # Key statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Spent", f"${df['amount'].sum():.2f}")
    with col2:
        st.metric("Average Expense", f"${df['amount'].mean():.2f}")
    with col3:
        st.metric("Highest Expense", f"${df['amount'].max():.2f}")
    with col4:
        st.metric("Lowest Expense", f"${df['amount'].min():.2f}")

    # Expense distribution
    col1, col2 = st.columns(2)

    with col1:
        # Histogram of expense amounts
        fig = px.histogram(df, x="amount", nbins=20, title="Distribution of Expense Amounts")
        fig.update_layout(xaxis_title="Amount ($)", yaxis_title="Frequency")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Box plot by category
        fig = px.box(df, x="category", y="amount", title="Expense Amount Distribution by Category")
        fig.update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)


def _show_trends_tab(df):
    """Display the trends analytics tab"""
    st.subheader("Spending Trends")

    # Monthly trend
    monthly_spending = df.groupby("month_name")["amount"].sum().reset_index()
    monthly_spending = monthly_spending.sort_values("month_name")  # Sort chronologically

    fig = px.line(monthly_spending, x="month_name", y="amount", title="Monthly Spending Trend", markers=True)
    fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Daily spending pattern
    daily_spending = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
    daily_spending.columns = ["date", "amount"]

    # Convert date column to datetime for proper plotting
    daily_spending["date"] = pd.to_datetime(daily_spending["date"])

    fig = px.scatter(daily_spending, x="date", y="amount", title="Daily Spending Pattern", trendline="lowess")
    fig.update_layout(xaxis_title="Date", yaxis_title="Amount ($)")
    st.plotly_chart(fig, use_container_width=True)


def _show_categories_tab(df):
    """Display the categories analytics tab"""
    st.subheader("Category Analysis")

    # Category spending
    category_spending = df.groupby("category")["amount"].agg(["sum", "count", "mean"]).reset_index()
    category_spending.columns = ["Category", "Total", "Count", "Average"]
    category_spending = category_spending.sort_values("Total", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart of category totals
        fig = px.bar(category_spending, x="Category", y="Total", title="Total Spending by Category")
        fig.update_layout(xaxis_title="Category", yaxis_title="Total Amount ($)")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Category summary table
        st.write("**Category Summary**")
        category_display = category_spending.copy()
        category_display["Total"] = category_display["Total"].apply(lambda x: f"${x:.2f}")
        category_display["Average"] = category_display["Average"].apply(lambda x: f"${x:.2f}")

        st.dataframe(category_display, hide_index=True, use_container_width=True)


def _show_patterns_tab(df):
    """Display the patterns analytics tab"""
    st.subheader("Spending Patterns")

    # Day of week analysis
    weekday_spending = df.groupby("weekday")["amount"].agg(["sum", "mean"]).reset_index()

    # Reorder days
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_spending["weekday"] = pd.Categorical(weekday_spending["weekday"], categories=day_order, ordered=True)
    weekday_spending = weekday_spending.sort_values("weekday")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(weekday_spending, x="weekday", y="sum", title="Total Spending by Day of Week")
        fig.update_layout(xaxis_title="Day of Week", yaxis_title="Total Amount ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(weekday_spending, x="weekday", y="mean", title="Average Spending by Day of Week")
        fig.update_layout(xaxis_title="Day of Week", yaxis_title="Average Amount ($)")
        st.plotly_chart(fig, use_container_width=True)

    # Monthly category heatmap
    try:
        # Create monthly category pivot table using string dates
        monthly_category_data = df.groupby(["month_name", "category"])["amount"].sum().reset_index()
        monthly_category_pivot = monthly_category_data.pivot(  # noqa: PD010
            index="month_name",
            columns="category",
            values="amount",
        ).fillna(0)

        if not monthly_category_pivot.empty:
            # Convert to numpy array for plotly
            z_data = monthly_category_pivot.values  # noqa: PD011
            x_labels = monthly_category_pivot.columns.tolist()
            y_labels = monthly_category_pivot.index.tolist()

            fig = px.imshow(
                z_data,
                x=x_labels,
                y=y_labels,
                title="Monthly Spending Heatmap by Category",
                aspect="auto",
                color_continuous_scale="Blues",
                labels=dict(x="Category", y="Month", color="Amount ($)"),  # noqa: C408
            )
            fig.update_layout(xaxis_title="Category", yaxis_title="Month")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for heatmap visualization")
    except Exception as e:
        st.warning(f"Could not generate heatmap: {str(e)}")  # noqa: RUF010
        st.info("This visualization requires data from multiple months and categories")

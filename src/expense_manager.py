from datetime import UTC, datetime

import pandas as pd
from tinydb import Query, TinyDB

from fake_data import get_fake_expenses
from utils.datetime_conversion import (
    convert_for_expense_tracker,
    get_current_date,
)


class ExpenseManager:
    """Enhanced expense management class with comprehensive functionality"""

    def __init__(self, db_path: str = "./src/data/expenses.json"):
        """Initialize the expense manager with database connection"""
        self.db = TinyDB(db_path)
        self.expenses_table = self.db.table("expenses")
        self.expenses = Query()

        # Common expense categories
        self.default_categories = [
            "Food",
            "Transport",
            "Bills",
            "Entertainment",
            "Health",
            "Shopping",
            "Education",
            "Travel",
            "Other",
        ]

    def add_expense(self, amount: float, description: str, category: str, date: str | None) -> bool:
        """Add a new expense to the database

        Args:
            amount: Expense amount
            description: Description of the expense
            category: Category of the expense
            date: Date of the expense (optional, defaults to today)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            date = get_current_date() if date is None else convert_for_expense_tracker(date)

            # Get next ID
            all_records = self.expenses_table.all()
            next_id = max([record.get("id", 0) for record in all_records], default=0) + 1

            expense_data = {
                "id": next_id,
                "amount": float(amount),
                "description": description.strip(),
                "category": category.capitalize(),
                "date": date,
                "created_at": datetime.now(tz=UTC).isoformat(),
            }

            self.expenses_table.insert(expense_data)
            return True  # noqa: TRY300

        except Exception as e:
            print(f"Error adding expense: {e}")  # noqa: T201
            return False

    def get_all_expenses(self) -> list[dict]:
        """Get all expenses from the database"""
        return self.expenses_table.all()

    def get_expenses_by_category(self, category: str) -> list[dict]:
        """Get expenses filtered by category"""
        return self.expenses_table.search(self.expenses.category == category.capitalize())

    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> list[dict]:
        """Get expenses within a date range"""
        start_date = convert_for_expense_tracker(start_date)
        end_date = convert_for_expense_tracker(end_date)

        return self.expenses_table.search((self.expenses.date >= start_date) & (self.expenses.date <= end_date))

    def get_expenses_by_month(self, year: int, month: int) -> list[dict]:
        """Get expenses for a specific month"""
        start_date = f"{year}-{month:02d}-01"

        # Calculate last day of month
        end_date = f"{year + 1}-01-01" if month == 12 else f"{year}-{month + 1:02d}-01"  # noqa: PLR2004

        return self.get_expenses_by_date_range(start_date, end_date)

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID"""
        try:
            result = self.expenses_table.remove(self.expenses.id == expense_id)
            return len(result) > 0
        except Exception as e:
            print(f"Error deleting expense: {e}")  # noqa: T201
            return False

    def update_expense(self, expense_id: int, **kwargs) -> bool:
        """Update an expense by ID"""
        try:
            update_data = {}

            if "amount" in kwargs:
                update_data["amount"] = float(kwargs["amount"])
            if "description" in kwargs:
                update_data["description"] = kwargs["description"].strip()
            if "category" in kwargs:
                update_data["category"] = kwargs["category"].capitalize()
            if "date" in kwargs:
                update_data["date"] = convert_for_expense_tracker(kwargs["date"])

            if update_data:
                update_data["updated_at"] = datetime.now(tz=UTC).isoformat()
                result = self.expenses_table.update(update_data, self.expenses.id == expense_id)
                return len(result) > 0

            return False  # noqa: TRY300

        except Exception as e:
            print(f"Error updating expense: {e}")  # noqa: T201
            return False

    def get_expense_by_id(self, expense_id: int) -> dict | None:
        """Get a specific expense by ID"""
        result = self.expenses_table.search(self.expenses.id == expense_id)
        return result[0] if result else None

    def get_total_expenses(self) -> float:
        """Get total amount of all expenses"""
        expenses = self.get_all_expenses()
        return sum(expense["amount"] for expense in expenses)

    def get_category_summary(self) -> dict[str, dict[str, float | int]]:
        """Get summary statistics by category"""
        expenses = self.get_all_expenses()
        summary = {}

        for expense in expenses:
            category = expense["category"]
            if category not in summary:
                summary[category] = {"total": 0, "count": 0, "average": 0}

            summary[category]["total"] += expense["amount"]
            summary[category]["count"] += 1

        # Calculate averages
        for category in summary:  # noqa: PLC0206
            if summary[category]["count"] > 0:
                summary[category]["average"] = summary[category]["total"] / summary[category]["count"]

        return summary

    def get_monthly_summary(self) -> pd.DataFrame:
        """Get monthly expense summary as DataFrame"""
        expenses = self.get_all_expenses()

        if not expenses:
            return pd.DataFrame()

        df = pd.DataFrame(expenses)  # noqa: PD901
        df["date"] = pd.to_datetime(df["date"])
        df["month_year"] = df["date"].dt.to_period("M")
        df["month_name"] = df["date"].dt.strftime("%B %Y")

        # Group by month and category
        monthly_summary = df.groupby(["month_name", "category"])["amount"].sum().reset_index()

        # Create pivot table
        pivot = monthly_summary.pivot_table(index="month_name", columns="category", values="amount").fillna(0)

        # Add total column
        pivot["Total"] = pivot.sum(axis=1)

        return pivot

    def get_recent_expenses(self, limit: int = 10) -> list[dict]:
        """Get most recent expenses"""
        expenses = self.get_all_expenses()

        # Sort by created_at timestamp (most recent first)
        expenses.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return expenses[:limit]

    def search_expenses(self, query: str) -> list[dict]:
        """Search expenses by description"""
        return self.expenses_table.search(
            self.expenses.description.matches(f".*{query}.*", flags=2),  # Case insensitive
        )

    def get_expenses_dataframe(self) -> pd.DataFrame:
        """Get all expenses as a pandas DataFrame"""
        expenses = self.get_all_expenses()

        if not expenses:
            return pd.DataFrame()

        df = pd.DataFrame(expenses)  # noqa: PD901
        df["date"] = pd.to_datetime(df["date"])

        return df

    def get_available_categories(self) -> list[str]:
        """Get list of all categories used in expenses"""
        expenses = self.get_all_expenses()
        categories = {expense["category"] for expense in expenses}

        # Combine with default categories
        all_categories = list(categories.union(set(self.default_categories)))

        return sorted(all_categories)

    def import_fake_data(self):
        """Import fake data for testing"""
        try:
            fake_expenses = get_fake_expenses()

            for expense in fake_expenses:
                self.add_expense(
                    amount=expense["amount"],
                    description=expense["description"],
                    category=expense["category"],
                    date=expense["date"],
                )

            return True  # noqa: TRY300

        except Exception as e:
            print(f"Error importing fake data: {e}")  # noqa: T201
            return False

    def clear_all_data(self) -> bool:
        """Clear all expense data (use with caution!)"""
        try:
            self.expenses_table.truncate()
            return True  # noqa: TRY300
        except Exception as e:
            print(f"Error clearing data: {e}")  # noqa: T201
            return False

    def export_to_csv(self, filename: str | None) -> str:
        """Export expenses to CSV file"""
        if filename is None:
            filename = f"expenses_export_{datetime.now(tz=UTC).strftime('%Y%m%d_%H%M%S')}.csv"

        df = self.get_expenses_dataframe()  # noqa: PD901

        if not df.empty:
            df.to_csv(filename, index=False)
            return filename

        return None

    def get_statistics(self) -> dict:
        """Get comprehensive expense statistics"""
        expenses = self.get_all_expenses()

        if not expenses:
            return {
                "total_expenses": 0,
                "total_amount": 0,
                "average_expense": 0,
                "expense_count": 0,
                "categories_count": 0,
                "date_range": None,
            }

        df = pd.DataFrame(expenses)  # noqa: PD901
        df["date"] = pd.to_datetime(df["date"])

        return {
            "total_expenses": len(expenses),
            "total_amount": df["amount"].sum(),
            "average_expense": df["amount"].mean(),
            "max_expense": df["amount"].max(),
            "min_expense": df["amount"].min(),
            "expense_count": len(expenses),
            "categories_count": df["category"].nunique(),
            "date_range": {
                "start": df["date"].min().strftime("%Y-%m-%d"),
                "end": df["date"].max().strftime("%Y-%m-%d"),
            },
            "most_expensive_category": df.groupby("category")["amount"].sum().idxmax(),
            "most_frequent_category": df["category"].mode().iloc[0] if not df["category"].mode().empty else None,
        }

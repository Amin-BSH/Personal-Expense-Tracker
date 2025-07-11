"""
Fake expense data generator for testing the expense tracker application.
Contains 50 realistic expense records with various categories, amounts, and dates.
"""

from datetime import datetime, timedelta
import random

# Generate fake expense data
fake_expenses = [
    {
        "amount": 25.50,
        "description": "Lunch at downtown cafe",
        "category": "Food",
        "date": "2024-01-15"
    },
    {
        "amount": 45.00,
        "description": "Gas station fill-up",
        "category": "Transport",
        "date": "2024-01-16"
    },
    {
        "amount": 12.99,
        "description": "Netflix monthly subscription",
        "category": "Entertainment",
        "date": "2024-01-16"
    },
    {
        "amount": 150.00,
        "description": "Electricity bill payment",
        "category": "Bills",
        "date": "2024-01-17"
    },
    {
        "amount": 8.50,
        "description": "Morning coffee and pastry",
        "category": "Food",
        "date": "2024-01-17"
    },
    {
        "amount": 75.30,
        "description": "Weekly grocery shopping",
        "category": "Food",
        "date": "2024-01-18"
    },
    {
        "amount": 15.00,
        "description": "Bus pass monthly renewal",
        "category": "Transport",
        "date": "2024-01-19"
    },
    {
        "amount": 89.99,
        "description": "Internet bill",
        "category": "Bills",
        "date": "2024-01-20"
    },
    {
        "amount": 22.75,
        "description": "Pizza delivery dinner",
        "category": "Food",
        "date": "2024-01-20"
    },
    {
        "amount": 35.00,
        "description": "Movie tickets for two",
        "category": "Entertainment",
        "date": "2024-01-21"
    },
    {
        "amount": 120.00,
        "description": "Phone bill payment",
        "category": "Bills",
        "date": "2024-01-22"
    },
    {
        "amount": 18.50,
        "description": "Lunch at work cafeteria",
        "category": "Food",
        "date": "2024-01-22"
    },
    {
        "amount": 65.00,
        "description": "Car maintenance - oil change",
        "category": "Transport",
        "date": "2024-01-23"
    },
    {
        "amount": 9.99,
        "description": "Spotify premium subscription",
        "category": "Entertainment",
        "date": "2024-01-24"
    },
    {
        "amount": 42.80,
        "description": "Dinner at Italian restaurant",
        "category": "Food",
        "date": "2024-01-24"
    },
    {
        "amount": 200.00,
        "description": "Rent payment",
        "category": "Bills",
        "date": "2024-01-25"
    },
    {
        "amount": 14.25,
        "description": "Fast food lunch",
        "category": "Food",
        "date": "2024-01-25"
    },
    {
        "amount": 28.00,
        "description": "Taxi ride to airport",
        "category": "Transport",
        "date": "2024-01-26"
    },
    {
        "amount": 55.00,
        "description": "Concert tickets",
        "category": "Entertainment",
        "date": "2024-01-27"
    },
    {
        "amount": 95.40,
        "description": "Weekly grocery shopping",
        "category": "Food",
        "date": "2024-01-28"
    },
    {
        "amount": 7.50,
        "description": "Coffee shop visit",
        "category": "Food",
        "date": "2024-01-29"
    },
    {
        "amount": 180.00,
        "description": "Car insurance payment",
        "category": "Bills",
        "date": "2024-01-30"
    },
    {
        "amount": 32.00,
        "description": "Uber ride downtown",
        "category": "Transport",
        "date": "2024-01-31"
    },
    {
        "amount": 16.75,
        "description": "Breakfast at diner",
        "category": "Food",
        "date": "2024-02-01"
    },
    {
        "amount": 24.99,
        "description": "Video game purchase",
        "category": "Entertainment",
        "date": "2024-02-02"
    },
    {
        "amount": 85.00,
        "description": "Water and sewer bill",
        "category": "Bills",
        "date": "2024-02-03"
    },
    {
        "amount": 19.50,
        "description": "Sandwich and drink",
        "category": "Food",
        "date": "2024-02-03"
    },
    {
        "amount": 50.00,
        "description": "Gas station payment",
        "category": "Transport",
        "date": "2024-02-04"
    },
    {
        "amount": 38.25,
        "description": "Thai food takeout",
        "category": "Food",
        "date": "2024-02-05"
    },
    {
        "amount": 15.99,
        "description": "Amazon Prime subscription",
        "category": "Entertainment",
        "date": "2024-02-06"
    },
    {
        "amount": 125.00,
        "description": "Credit card payment",
        "category": "Bills",
        "date": "2024-02-07"
    },
    {
        "amount": 11.00,
        "description": "Coffee and muffin",
        "category": "Food",
        "date": "2024-02-07"
    },
    {
        "amount": 72.50,
        "description": "Grocery store shopping",
        "category": "Food",
        "date": "2024-02-08"
    },
    {
        "amount": 25.00,
        "description": "Parking fee downtown",
        "category": "Transport",
        "date": "2024-02-09"
    },
    {
        "amount": 45.00,
        "description": "Streaming service bundle",
        "category": "Entertainment",
        "date": "2024-02-10"
    },
    {
        "amount": 160.00,
        "description": "Heating bill",
        "category": "Bills",
        "date": "2024-02-11"
    },
    {
        "amount": 29.75,
        "description": "Chinese food delivery",
        "category": "Food",
        "date": "2024-02-11"
    },
    {
        "amount": 40.00,
        "description": "Train ticket to city",
        "category": "Transport",
        "date": "2024-02-12"
    },
    {
        "amount": 13.50,
        "description": "Fast casual lunch",
        "category": "Food",
        "date": "2024-02-13"
    },
    {
        "amount": 78.00,
        "description": "Gym membership monthly",
        "category": "Health",
        "date": "2024-02-14"
    },
    {
        "amount": 220.00,
        "description": "Home insurance payment",
        "category": "Bills",
        "date": "2024-02-15"
    },
    {
        "amount": 21.25,
        "description": "Brunch at local cafe",
        "category": "Food",
        "date": "2024-02-15"
    },
    {
        "amount": 35.00,
        "description": "Car wash and detailing",
        "category": "Transport",
        "date": "2024-02-16"
    },
    {
        "amount": 52.80,
        "description": "Date night dinner",
        "category": "Food",
        "date": "2024-02-17"
    },
    {
        "amount": 19.99,
        "description": "Book purchase online",
        "category": "Education",
        "date": "2024-02-18"
    },
    {
        "amount": 95.00,
        "description": "Utility bill payment",
        "category": "Bills",
        "date": "2024-02-19"
    },
    {
        "amount": 17.00,
        "description": "Lunch at food truck",
        "category": "Food",
        "date": "2024-02-19"
    },
    {
        "amount": 60.00,
        "description": "Metro card refill",
        "category": "Transport",
        "date": "2024-02-20"
    },
    {
        "amount": 33.50,
        "description": "Mexican restaurant dinner",
        "category": "Food",
        "date": "2024-02-21"
    },
    {
        "amount": 12.00,
        "description": "Movie rental online",
        "category": "Entertainment",
        "date": "2024-02-22"
    }
]

def get_fake_expenses():
    """
    Returns a list of 50 fake expense records for testing.

    Returns:
        list: List of dictionaries containing expense data
    """
    return fake_expenses

def get_expenses_by_category(category):
    """
    Filter fake expenses by category.

    Args:
        category (str): Category to filter by

    Returns:
        list: Filtered list of expenses
    """
    return [expense for expense in fake_expenses if expense['category'] == category]

def get_expenses_by_date_range(start_date, end_date):
    """
    Filter fake expenses by date range.

    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format

    Returns:
        list: Filtered list of expenses
    """
    return [
        expense for expense in fake_expenses
        if start_date <= expense['date'] <= end_date
    ]

def get_total_amount():
    """
    Calculate total amount of all fake expenses.

    Returns:
        float: Total amount
    """
    return sum(expense['amount'] for expense in fake_expenses)

def get_category_summary():
    """
    Get summary of expenses by category.

    Returns:
        dict: Dictionary with category totals
    """
    summary = {}
    for expense in fake_expenses:
        category = expense['category']
        if category not in summary:
            summary[category] = {'total': 0, 'count': 0}
        summary[category]['total'] += expense['amount']
        summary[category]['count'] += 1
    return summary

# Statistics about the fake data
TOTAL_EXPENSES = len(fake_expenses)
TOTAL_AMOUNT = get_total_amount()
CATEGORIES = list(set(expense['category'] for expense in fake_expenses))
DATE_RANGE = {
    'start': min(expense['date'] for expense in fake_expenses),
    'end': max(expense['date'] for expense in fake_expenses)
}

if __name__ == "__main__":
    print(f"Fake Expense Data Summary:")
    print(f"Total Expenses: {TOTAL_EXPENSES}")
    print(f"Total Amount: ${TOTAL_AMOUNT:.2f}")
    print(f"Categories: {CATEGORIES}")
    print(f"Date Range: {DATE_RANGE['start']} to {DATE_RANGE['end']}")
    print(f"\nCategory Summary:")
    for category, data in get_category_summary().items():
        avg = data['total'] / data['count']
        print(f"  {category}: ${data['total']:.2f} ({data['count']} expenses, avg: ${avg:.2f})")

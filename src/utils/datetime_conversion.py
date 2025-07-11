"""
DateTime conversion utilities for expense tracker
"""

from datetime import datetime, date, timedelta
import re


def convert_to_standard_date(date_input, input_format=None):
    """
    Convert various date formats to standard YYYY-MM-DD format.

    Args:
        date_input: Date in various formats (string, datetime object, etc.)
        input_format: Optional format string if known

    Returns:
        str: Date in YYYY-MM-DD format
    """

    # If it's already a datetime object
    if isinstance(date_input, datetime):
        return date_input.strftime("%Y-%m-%d")

    # If it's a date object
    if isinstance(date_input, date):
        return date_input.strftime("%Y-%m-%d")

    # If it's a string, try different formats
    if isinstance(date_input, str):
        # Remove extra whitespace
        date_input = date_input.strip()

        # If format is provided, use it directly
        if input_format:
            try:
                dt = datetime.strptime(date_input, input_format)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

        # Try common formats automatically
        common_formats = [
            "%Y-%m-%d",  # 2024-01-15 (already correct)
            "%d/%m/%Y",  # 15/01/2024
            "%m/%d/%Y",  # 01/15/2024
            "%d-%m-%Y",  # 15-01-2024
            "%m-%d-%Y",  # 01-15-2024
            "%Y/%m/%d",  # 2024/01/15
            "%d.%m.%Y",  # 15.01.2024
            "%Y.%m.%d",  # 2024.01.15
            "%B %d, %Y",  # January 15, 2024
            "%b %d, %Y",  # Jan 15, 2024
            "%d %B %Y",  # 15 January 2024
            "%d %b %Y",  # 15 Jan 2024
            "%Y-%m-%d %H:%M:%S",  # 2024-01-15 14:30:00
            "%Y-%m-%d %H:%M",  # 2024-01-15 14:30
            "%d/%m/%Y %H:%M:%S",  # 15/01/2024 14:30:00
            "%m/%d/%Y %H:%M:%S",  # 01/15/2024 14:30:00
        ]

        for fmt in common_formats:
            try:
                dt = datetime.strptime(date_input, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # Try to parse with regex for flexible formats
        return parse_with_regex(date_input)

    raise ValueError(f"Cannot convert {date_input} to standard date format")


def parse_with_regex(date_string):
    """
    Parse date using regex patterns for flexible input.

    Args:
        date_string (str): Date string to parse

    Returns:
        str: Date in YYYY-MM-DD format
    """

    # Pattern for YYYY-MM-DD or YYYY/MM/DD or YYYY.MM.DD
    pattern1 = r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})"
    match = re.match(pattern1, date_string)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"

    # Pattern for DD-MM-YYYY or DD/MM/YYYY or DD.MM.YYYY
    pattern2 = r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})"
    match = re.match(pattern2, date_string)
    if match:
        day, month, year = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"

    raise ValueError(f"Cannot parse date: {date_string}")


def convert_for_expense_tracker(date_input):
    """
    Specific function for expense tracker to ensure consistent date format.

    Args:
        date_input: Date in any supported format

    Returns:
        str: Date in YYYY-MM-DD format for database storage
    """

    # Handle None or empty input
    if not date_input:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        return convert_to_standard_date(date_input)
    except ValueError:
        # If conversion fails, use current date
        print(f"Warning: Could not parse date '{date_input}', using current date")
        return datetime.now().strftime("%Y-%m-%d")


def validate_date_format(date_string):
    """
    Validate if a date string is in YYYY-MM-DD format.

    Args:
        date_string (str): Date string to validate

    Returns:
        bool: True if valid YYYY-MM-DD format
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_current_date():
    """Get current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

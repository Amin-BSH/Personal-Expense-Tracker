"""Configuration settings for the Personal Expense Tracker"""

from pathlib import Path

# Application settings
APP_NAME = "Personal Expense Tracker"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "A modern, modular expense tracking application"

# Database settings
DATABASE_DIR = Path(__file__).parent / "data"
DATABASE_FILE = DATABASE_DIR / "expenses.json"

# Default categories
DEFAULT_CATEGORIES = [
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

# UI settings
DEFAULT_CURRENCY = "USD"
DEFAULT_CURRENCY_SYMBOL = "$"
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%B %d, %Y"

# Chart settings
CHART_COLOR_PALETTE = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#FFEAA7",
    "#DDA0DD",
    "#98D8C8",
    "#F7DC6F",
    "#AED6F1",
    "#95A5A6",
]

# Export settings
EXPORT_DIR = Path(__file__).parent / "exports"
CSV_FILENAME_FORMAT = "expenses_export_{timestamp}.csv"

# Sample data settings
SAMPLE_DATA_COUNT = 50
SAMPLE_DATE_RANGE_DAYS = 365

# Validation settings
MIN_EXPENSE_AMOUNT = 0.01
MAX_EXPENSE_AMOUNT = 999999.99
MAX_DESCRIPTION_LENGTH = 200
MAX_CATEGORY_LENGTH = 50

# Analytics settings
RECENT_EXPENSES_COUNT = 5
CHART_HEIGHT = 400
CHART_WIDTH = 600


# Create necessary directories
def ensure_directories():
    """Ensure all necessary directories exist"""
    DATABASE_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)


# Initialize directories when module is imported
ensure_directories()

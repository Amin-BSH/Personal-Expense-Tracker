# 💰 Personal Expense Tracker

A modern, modular personal expense tracking application built with Streamlit and Python. Track your expenses, visualize spending patterns, and gain insights into your financial habits.

## 🚀 Features

- **Dashboard**: Overview of your spending with key metrics and recent expenses
- **Add Expenses**: Easy expense entry with custom categories
- **View & Edit**: Browse, search, filter, and edit your expenses
- **Analytics**: Comprehensive charts and spending pattern analysis
- **Data Management**: Import sample data, export to CSV, and manage your database

## 📁 Project Structure

```
src/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── expense_manager.py     # Core expense management logic
├── fake_data.py          # Sample data generation
├── ui/                   # User interface components
│   ├── __init__.py
│   ├── dashboard.py      # Dashboard page
│   ├── add_expense.py    # Add expense page
│   ├── view_expenses.py  # View/edit expenses page
│   ├── analytics.py      # Analytics and charts page
│   ├── manage_data.py    # Data management page
│   ├── styles.py         # CSS styles and theming
│   └── utils.py          # UI utility functions
├── utils/                # Utility modules
│   └── datetime_conversion.py
└── data/                 # Database storage
    └── expenses.json
```

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install streamlit pandas plotly tinydb beautifultable statsmodels
   ```

3. **Run the application:**
   ```bash
   streamlit run src/app.py
   ```

## 📋 Requirements

- Python 3.7+
- streamlit
- pandas
- plotly
- tinydb
- beautifultable
- statsmodels

## 🎯 Quick Start

1. **Launch the app** and navigate to the Dashboard
2. **Add your first expense** using the "Add Expense" page
3. **Import sample data** from the "Manage Data" page to explore features
4. **View analytics** to see spending patterns and trends
5. **Export your data** as CSV when needed

## 🔧 Configuration

The application can be configured through `src/config.py`:

- **Database location**: Change `DATABASE_FILE` path
- **Default categories**: Modify `DEFAULT_CATEGORIES` list
- **UI settings**: Adjust colors, formats, and display options
- **Validation rules**: Set min/max amounts and field lengths

## 📊 Analytics Features

- **Overview**: Key statistics and expense distribution
- **Trends**: Monthly spending trends with trendlines
- **Categories**: Category-wise analysis and breakdowns
- **Patterns**: Day-of-week analysis and spending heatmaps

## 🔒 Data Management

- **Local Storage**: All data stored locally in JSON format
- **Export/Import**: CSV export functionality
- **Sample Data**: Generate realistic test data
- **Data Validation**: Input validation and error handling

## 🎨 Architecture

The application follows a modular architecture:

- **Separation of Concerns**: UI components separated from business logic
- **Reusable Components**: Modular UI components for easy maintenance
- **Configuration Management**: Centralized settings and constants
- **Error Handling**: Comprehensive error handling throughout

## 🚀 Running the Application

```bash
streamlit run src/app.py
```
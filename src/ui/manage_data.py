"""Data management page component for the expense tracker"""

import streamlit as st


def show_manage_data(manager, show_success_message, show_error_message):
    """Display the data management page"""
    st.header("🔧 Manage Data")

    # Data statistics
    stats = manager.get_statistics()

    col1, col2 = st.columns(2)

    with col1:
        _show_database_statistics(stats)

    with col2:
        _show_quick_actions(manager, show_success_message, show_error_message)

    st.divider()

    # Dangerous operations
    _show_dangerous_operations(manager, show_success_message, show_error_message)


def _show_database_statistics(stats):
    """Display database statistics"""
    st.subheader("Database Statistics")
    st.write(f"**Total Expenses:** {stats['total_expenses']}")
    st.write(f"**Total Amount:** ${stats['total_amount']:.2f}")
    st.write(f"**Categories:** {stats['categories_count']}")

    if stats["date_range"]:
        st.write(f"**Date Range:** {stats['date_range']['start']} to {stats['date_range']['end']}")


def _show_quick_actions(manager, show_success_message, show_error_message):
    """Display quick action buttons"""
    st.subheader("Quick Actions")

    # Import fake data
    if st.button("Import Sample Data", help="Add 50 sample expenses for testing"):
        if manager.import_fake_data():
            show_success_message("Sample data imported successfully!")
            st.rerun()
        else:
            show_error_message("Failed to import sample data")

    # Export data
    if st.button("Export to CSV", help="Download all expenses as CSV"):
        filename = manager.export_to_csv()
        if filename:
            show_success_message(f"Data exported to {filename}")
        else:
            show_error_message("Failed to export data")


def _show_dangerous_operations(manager, show_success_message, show_error_message):
    """Display dangerous operations section"""
    st.subheader("⚠️ Dangerous Operations")
    st.warning("These operations cannot be undone!")

    # Clear all data
    if st.button("Clear All Data", type="secondary", help="Delete all expenses permanently"):
        if st.session_state.get("confirm_clear", False):
            if manager.clear_all_data():
                show_success_message("All data cleared successfully")
                st.session_state["confirm_clear"] = False
                st.rerun()
            else:
                show_error_message("Failed to clear data")
        else:
            st.session_state["confirm_clear"] = True
            st.error("Click again to confirm deletion of all data")

    # Reset confirmation state
    if st.session_state.get("confirm_clear", False) and st.button("Cancel", type="primary"):
        st.session_state["confirm_clear"] = False
        st.rerun()

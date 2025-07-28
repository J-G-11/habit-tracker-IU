from datetime import date, datetime, timedelta
import pytest
from habit import Habit
import db
import sqlite3

TEST_DB = "test_database.db"


def setup_module(module):
    """
    initializing the test database
    :param module:
    :return:
    """
    db.db_name = TEST_DB
    db.initialize_db()

    # lets add a testing habit
    test_habit = Habit(
        name="Test Habit",
        description="A test habit for daily tracking",
        time_period="d"
    )

    # get the ID of our new testing habit
    habit_ID = test_habit.habit_ID

    # lets fake some log entries
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()

        # Clear today's log to avoid interference
        cursor.execute("DELETE FROM habit_log WHERE habit_ID = ?", (habit_ID,))
        cursor.execute("DELETE FROM habit_streak WHERE habit_ID = ?", (habit_ID,))

        # insert fake logs for testing
        cursor.executemany("""
            INSERT INTO habit_log (habit_ID, 
                                habit_completed, 
                                habit_date_created)
            VALUES (?, ?, ?)
        """, [(habit_ID, True, "07/01/2025"),
              (habit_ID, True, "07/02/2025"),
              (habit_ID, True, "07/03/2025"),
              (habit_ID, True, "07/04/2025"),
              (habit_ID, True, "07/07/2025"),
              (habit_ID, True, "07/08/2025"),
              (habit_ID, True, "07/09/2025"),
              (habit_ID, True, "07/11/2025"),
              (habit_ID, True, "07/12/2025"),
              (habit_ID, True, "07/13/2025"),
              (habit_ID, True, "07/14/2025"),
              (habit_ID, True, "07/15/2025"),
              (habit_ID, True, "07/20/2025"),
              (habit_ID, True, "07/21/2025"),
              (habit_ID, True, "07/24/2025"),
              (habit_ID, True, "07/25/2025")
              ]
                           )
    cursor.close()
    conn.commit()


def test_update_streak_in_db_daily():
    """Test if streak updates correctly for a daily habit."""
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()

        # Get test habit ID
        cursor.execute("SELECT habit_ID "
                       "FROM habit_info "
                       "WHERE habit_name = ?",
                       ("Test Habit",))
        habit_ID = cursor.fetchone()[0]

    # Run the streak update logic
    db.update_streak_in_db(habit_ID)

    # Check if streak incremented
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT habit_counter, "
                       "habit_counter_max "
                       "FROM habit_streak "
                       "WHERE habit_ID = ?",
                       (habit_ID,))
        current, maximum = cursor.fetchone()
        cursor.close()

    assert current == 1, "Current streak should be 1"
    assert maximum == 4, "Max streak should be updated to 4"

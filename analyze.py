# ANALYZE.PY
"""For increased user-friendliness the two functionalities “Analyze” and “View” are
separate in the main menu. However, they both refer to the analyze.py-file with the
associated functions.
When calling the “View” option in the main menu, users will be presented to choose
from three different options. First, they can view a list of all saved habits and their
current streak information. Second, they can choose to view a list of all saved habits
of a given periodicity and their current streak information. Third, users can view the
log information for a given habit to see the dates and times they checked off the
habit.
When selecting the "Analyze" option from the main menu, users will have two
options. First, they can analyze and view the habit with the longest streak for a given
periodicity. Second, they can analyze and view the longest overall streak for a given
habit and compare it to its current streak.
"""

from db import db_name
import sqlite3


def view_habits_by_time_period(time_period=None):
    """
        Displays all habits and their current streaks, filtered optionally by time period.

    :param time_period: str, optional; Filter for the habit time period.
                                     'd' for daily habits, 'w' for weekly habits.
                                     If not provided, shows all habits.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            if time_period in ("d", "w"):
                cursor.execute("""
                                SELECT habit_info.habit_ID, 
                                habit_info.habit_name, 
                                habit_info.habit_time_period, 
                                habit_streak.habit_counter 
                                FROM habit_info JOIN habit_streak 
                                ON habit_info.habit_ID = habit_streak.habit_ID
                                WHERE habit_info.habit_time_period = ?
                            """, (time_period,))
            else:
                cursor.execute("""
                                SELECT habit_info.habit_ID, 
                                habit_info.habit_name, 
                                habit_info.habit_time_period, 
                                habit_streak.habit_counter
                                FROM habit_info JOIN habit_streak 
                                ON habit_info.habit_ID = habit_streak.habit_ID
                            """)

            rows = cursor.fetchall()
            if not rows:
                print("\nNo matching habits found.")
                return

            print("\n--- Habits and Streaks ---")
            for row in rows:
                habit_ID, habit_name, habit_time_period, habit_counter = row
                period_str = "Daily" if time_period == "d" else "Weekly"
                print(f"[{habit_ID}] {habit_name} ({period_str}) "
                      f"– Current streak: {habit_counter}")
    except sqlite3.OperationalError as e:
        print("Failed to retrieve habit streak information:", e)


def analyze_current_streak_max(habit_ID=None, time_period=None):
    """
        Displays the longest streaks for habits, filtered by habit ID or time period.
    :param habit_ID: (int, optional) The ID of a specific habit to analyze.
                                  If provided, only this habit is analyzed.
    :param time_period: (str, optional) Time period filter, either 'd' for daily or 'w' for weekly.
                                     If provided and habit_ID is None, all habits of this type are shown.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            if habit_ID is not None:
                cursor.execute("""
                                SELECT habit_info.habit_ID,
                                       habit_info.habit_name,
                                       habit_info.habit_time_period,
                                       habit_streak.habit_counter_max
                                FROM habit_info
                                JOIN habit_streak 
                                ON habit_info.habit_ID = habit_streak.habit_ID
                                WHERE habit_info.habit_ID = ?
                            """, (habit_ID,))
            elif time_period in ("d", "w"):
                cursor.execute("""
                                SELECT habit_info.habit_ID, 
                                habit_info.habit_name, 
                                habit_info.habit_time_period, 
                                habit_streak.habit_counter_max
                                FROM habit_info 
                                JOIN habit_streak 
                                ON habit_info.habit_ID = habit_streak.habit_ID
                                WHERE habit_info.habit_time_period = ?
                            """, (time_period,))
            else:
                cursor.execute("""
                                SELECT habit_info.habit_ID, 
                                habit_info.habit_name, 
                                habit_info.habit_time_period,
                                habit_streak.habit_counter_max
                                FROM habit_info 
                                JOIN habit_streak 
                                ON habit_info.habit_ID = habit_streak.habit_ID
                            """)

            rows = cursor.fetchall()
            if not rows:
                print("\nNo matching habits found.")
                return

            print("\n--- Habits and Streaks ---")
            for row in rows:
                habit_ID, habit_name, habit_time_period, habit_counter_max = row
                period_str = "Daily" if habit_time_period == "d" else "Weekly"
                print(f"[{habit_ID}] {habit_name} ({period_str}) "
                      f"Longest streak: {habit_counter_max}")
    except sqlite3.OperationalError as e:
        print("Failed to retrieve habit streak information:", e)

import sqlite3
from datetime import datetime, timedelta, date

db_name = "main.db"


# Initialize the databases if not already exists

def initialize_db():
    """
        Initializes the database and creates necessary tables if they do not already exist:
        - habit_info
        - habit_log
        - habit_streak
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS habit_info (
                                       habit_ID INTEGER PRIMARY KEY,
                                       habit_name TEXT NOT NULL, 
                                       habit_description TEXT NOT NULL,
                                       habit_time_period TEXT NOT NULL,
                                       habit_date_created DATE 
                                ) 
                            """)
            print("Created table: habit_info")
            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS habit_log (
                                        habit_ID INTEGER,
                                        habit_completed BOOLEAN,
                                        habit_date_created DATE,
                                        FOREIGN KEY (habit_ID) REFERENCES habit_info(habit_ID) 
                                ) 
                             """)
            print("Created table: habit_log")
            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS habit_streak (
                                        habit_ID INTEGER,
                                        habit_counter INTEGER DEFAULT 0,
                                        habit_counter_max INTEGER DEFAULT 0,
                                        FOREIGN KEY (habit_ID) REFERENCES habit_info(habit_ID)
                                )
                             """)
            print("Created table: habit_streak")

            conn.commit()

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


# methods to add new information to the tables and classes

def add_habit_info(habit_name, habit_description, habit_time_period, habit_date_created):
    """
         Inserts a new habit into the 'habit_info' table.

    :return: int: The ID of the newly created habit.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                                INSERT INTO habit_info(habit_name, habit_description,
                                habit_time_period, habit_date_created)
                                VALUES (?, ?, ?, ?) 
                            """,
                           (habit_name, habit_description, habit_time_period, habit_date_created))
            conn.commit()
        # get the id of the last inserted row
        return cursor.lastrowid

    except sqlite3.OperationalError as e:
        print("Failed to add data for habit_info to the database:", e)


def add_habit_log(habit_ID, habit_completed, habit_date_created):
    """
         Logs the completion status of a habit for a given date in 'habit_log'.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                            INSERT INTO habit_log(habit_ID, habit_completed,
                            habit_date_created)
                            VALUES (?, ?, ?)
                            """,
                           (habit_ID, habit_completed, habit_date_created))
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Failed to add data for habit_log to the database:", e)


def add_habit_streak(habit_ID, habit_counter, habit_counter_max):
    """
         Initializes streak tracking for a habit in 'habit_streak'.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                            INSERT INTO habit_streak(habit_ID, habit_counter,
                            habit_counter_max)
                            VALUES (?, ?, ?)
                            """,
                           (habit_ID, habit_counter, habit_counter_max))
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Failed to add data for habit_log to the database:", e)


def add_habit():
    """
        Adds a habit to all relevant tables (habit_info, habit_log, habit_streak).

    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            # add the new habit in habit_info

            habit_ID = add_habit_info(habit_name, habit_description, habit_time_period, habit_date_created)
            print(f"Created a new habit in habit_log with the ID {habit_ID}")

            # add the new habit in habit_log

            add_habit_log(habit_ID, habit_completed, habit_date_created)

            # add the new habit in habit_streak

            add_habit_streak(habit_ID, habit_counter, habit_counter_max)


    except sqlite3.OperationalError as e:
        print("Failed to add habit to the database:", e)


# method to fetch all current habits for selection

def get_all_habits():
    """
         Retrieves all existing habits' IDs and names from 'habit_info'.
    :return: list[tuple]: List of (habit_ID, habit_name) tuples.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habit_ID, habit_name FROM habit_info")
            return cursor.fetchall()
    except sqlite3.OperationalError as e:
        print("Failed to fetch habits:", e)
        return []


# methods to delete data from all the tables and the class

def delete_habit_from_db(habit_ID):
    """
    Deletes a habit and all its related entries from all tables.
    :param habit_ID: The ID of the habit to be deleted.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM habit_log WHERE habit_ID = ?", (habit_ID,))
            cursor.execute("DELETE FROM habit_streak WHERE habit_ID = ?", (habit_ID,))
            cursor.execute("DELETE FROM habit_info WHERE habit_ID = ?", (habit_ID,))

            conn.commit()
            # print(f"Habit {habit_ID} and associated data successfully deleted.")
    except sqlite3.OperationalError as e:
        print("Failed to delete habit:", e)


# methods to print our three db tables & view streak information

def print_table(habit_info, db_name):
    """
     Prints the contents of a given table from the database.
    :param habit_info: table_name (str): The name of the table to be printed.
    :param db_name: db_name (str): The name of the SQLite database.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {habit_info}")
            rows = cursor.fetchall()

            if rows:
                print(f"\n--- Contents of table: {habit_info} ---")
                for row in rows:
                    print(row)
            else:
                print(f"\nTable '{habit_info}' is empty.")
    except sqlite3.OperationalError as e:
        print(f"Error reading table '{habit_info}':", e)


def print_table(habit_log, db_name):
    """
         Prints the contents of a given table from the database.
        :param habit_log: table_name (str): The name of the table to be printed.
        :param db_name: db_name (str): The name of the SQLite database.
        :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {habit_log}")
            rows = cursor.fetchall()

            if rows:
                print(f"\n--- Contents of table: {habit_log} ---")
                for row in rows:
                    print(row)
            else:
                print(f"\nTable '{habit_log}' is empty.")
    except sqlite3.OperationalError as e:
        print(f"Error reading table '{habit_log}':", e)


def print_table(habit_streak, db_name):
    """
        Prints the contents of a given table from the database.
        :param habit_streak: table_name (str): The name of the table to be printed.
        :param db_name: db_name (str): The name of the SQLite database.
        :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {habit_streak}")
            rows = cursor.fetchall()

            if rows:
                print(f"\n--- Contents of table: {habit_streak} ---")
                for row in rows:
                    print(row)
            else:
                print(f"\nTable '{habit_streak}' is empty.")
    except sqlite3.OperationalError as e:
        print(f"Error reading table '{habit_streak}':", e)



# methods for checking off habit

def check_off_habit_in_db(habit_ID):
    """
    Marks a habit as completed for today's date by adding a row to 'habit_log'.
    :param habit_ID: The ID of the habit being marked as completed.
    :return:
    """
    today = date.today().strftime("%m/%d/%Y")
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Insert new entry into habit_log
            cursor.execute("""
                INSERT INTO habit_log (habit_ID, habit_completed, habit_date_created)
                VALUES (?, ?, ?)
            """, (habit_ID, True, today))

            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to mark habit as completed:", e)


def update_streak_in_db(habit_ID):
    """
    Updates the current and maximum streak counters for a habit based on the
    last two completion dates and the habit's time period.
    :param habit_ID: The ID of the habit whose streak is being updated.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # 1. Get the last completion date
            cursor.execute("""
                    SELECT habit_date_created 
                    FROM habit_log 
                    WHERE habit_ID = ? 
                    ORDER BY habit_date_created DESC LIMIT 2
                """, (habit_ID,))
            dates = cursor.fetchall()

            if len(dates) < 2:
                # First completion or only one record: start streak
                cursor.execute("""
                        UPDATE habit_streak 
                        SET habit_counter = 1 
                        WHERE habit_ID = ?
                    """, (habit_ID,))
                conn.commit()
                return

            last_date = datetime.strptime(dates[1][0], "%m/%d/%Y").date()
            today = date.today()

            # 2. Get time_period (d or w)
            cursor.execute("""
                    SELECT habit_time_period 
                    FROM habit_info 
                    WHERE habit_ID = ?
                """, (habit_ID,))
            time_period = cursor.fetchone()[0]

            # 3. Define valid gap
            if time_period == 'd':
                expected_date = last_date + timedelta(days=1)
            elif time_period == 'w':
                expected_date = last_date + timedelta(weeks=1)
            else:
                print("Invalid time period.")
                return

            # 4. Compare and update streak
            if today == expected_date:
                # Increment streak
                cursor.execute("""
                        UPDATE habit_streak 
                        SET habit_counter = habit_counter + 1 
                        WHERE habit_ID = ?
                    """, (habit_ID,))
            else:
                # Reset streak
                cursor.execute("""
                        UPDATE habit_streak 
                        SET habit_counter = 1 
                        WHERE habit_ID = ?
                    """, (habit_ID,))

            # 5. Update max if needed
            cursor.execute("""
                    UPDATE habit_streak 
                    SET habit_counter_max = MAX(habit_counter, habit_counter_max)
                    WHERE habit_ID = ?
                """, (habit_ID,))

            conn.commit()
            cursor.close()
            print(f"Streak updated for habit ID {habit_ID}.")

    except sqlite3.OperationalError as e:
        print("Error while updating streak:", e)


def update_habit_info(habit_ID, new_habit_name, new_habit_description):
    """
    Updates the name and description of a habit in 'habit_info'.
    :param habit_ID: ID of the habit to update.
    :param new_habit_name: New name for the habit.
    :param new_habit_description: New description for the habit.
    :return:
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                UPDATE habit_info
                SET habit_name = ?,
                habit_description = ?
                WHERE habit_ID = ?""",
                           (habit_ID, new_habit_name, new_habit_description))
            conn.commit()
            print(f"Habit {habit_ID} successfully updated in habit_info.")
    except sqlite3.OperationalError as e:
        print("Error while editing habit_info:", e)

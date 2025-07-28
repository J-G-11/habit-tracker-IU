from datetime import date
import db


class Habit:
    """
    A class representing a habit tracked by the user. This habit class will serve as the template for our different habits. Using the __init__ constructor, the attributes
and methods will be defined.

    This class allows creation, tracking, and editing of habits. It automatically
    adds the habit to the database in the three tables habit_info, habit_log and habit_streak.

    Attributes:
        habit_ID (int): identifier assigned by the database.
        habit_name (str): Name of the habit.
        habit_description (str): Description of the habit.
        habit_time_period (str): Time interval for habit ('d' for daily, 'w' for weekly).
        habit_date_created (str): Date the habit was created (MM/DD/YYYY).
        habit_counter (int): Current streak count.
        habit_counter_max (int): Maximum streak count.
        habit_completed (bool): Whether the habit is marked completed for the current period.
    """

    # initiating the class
    def __init__(self, name: str, description: str,
                 time_period: str, completed = False):
        self.habit_ID = None
        self.habit_name = name
        self.habit_description = description
        self.habit_time_period = time_period
        self.habit_date_created = date.today().strftime("%m/%d/%Y")
        self.habit_counter = 0
        self.habit_counter_max = 0
        self.habit_completed = completed

        self.add_habit_object()


    def __str__(self):
        """
            Return a readable string representation of the Habit object.
        """
        return f"<Habit {self.habit_ID}: {self.habit_name} ({self.habit_time_period})>"


    # defining the method to add a new habit in the database using a db function
    def add_habit_object(self):
        """
            Add the habit's details to the database.
        """
        self.habit_ID = db.add_habit_info(
            self.habit_name,
            self.habit_description,
            self.habit_time_period,
            self.habit_date_created
        )
        db.add_habit_log(
            self.habit_ID,
            self.habit_completed,
            self.habit_date_created
        )

        db.add_habit_streak(
            self.habit_ID,
            self.habit_counter,
            self.habit_counter_max
        )




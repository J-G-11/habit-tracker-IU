# Habit tracker Main file
"""
The main.py file will lead the user through the menu and allowing them to access
different functions of the program. Furthermore, it will provide a welcome and
goodbye message.
To implement we will use the library “questionary” (Version 2.1.0, Bocklisch & Cross,
2024).This allows a smooth transition between menu points for users to select using
their arrow buttons. Once inside the menu, users can check off one of their habits,
add new habits, edit or delete existing habits, analyze habits, view their current habits
and streaks, or exit the program.
Users can access habit objects and related log data stored in the database.db file via
the main.py file using getter functions. They can also create new objects via the
habits.py file and analyze habit data using the functions in the analyze.py file.
When interacting with the CLI, the main.py-file will provide written instructions and
appropriate feedback to the user.
"""

import questionary
import db
import analyze
#import habit
from habit import Habit


def main_menu():
    """
    Display the main menu to the user using a CLI interface powered by questionary.
    This function acts as the main navigation hub for the user, allowing them to:
    - Check off a habit for today
    - Create a new habit
    - Edit or delete existing habits
    - View current habits (by type)
    - Analyze habit streaks
    - Exit the program

    After performing any action, the user is returned to the main menu unless they choose to exit.
    :return:
    """
    print("Hi there, welcome to your personal habit tracking app!")
    choice = questionary.select(
        "Choose an action:",
        choices=[
            "Check off habit for today",
            "Create new habit",
            "Edit existing habit",
            "Delete existing habit",
            "View current habits",
            "Analyze current habits",
            "Exit the program"
        ]
    ).ask()

    if choice == "Check off habit for today":
        check_off_habit()
        main_menu()
    elif choice == "Create new habit":
        add_new_habit()
        main_menu()
    elif choice == "Edit existing habit":
        edit_existing_habit()
        main_menu()
    elif choice == "Delete existing habit":
        delete_existing_habit()
        main_menu()
    elif choice == "View current habits":
        second_choice = questionary.select(
            "Which habits & streaks do you want to display?",
            choices=[
                "Show me all habits",
                "Show me only the daily habits",
                "Show me only the weekly habits",
                "Go back to main menu"
            ]
        ).ask()
        if second_choice == "Show me all habits":
            analyze.view_habits_by_time_period()
            main_menu()
        elif second_choice == "Show me only the daily habits":
            analyze.view_habits_by_time_period("d")
            main_menu()
        elif second_choice == "Show me only the weekly habits":
            analyze.view_habits_by_time_period("w")
            main_menu()
        elif second_choice == "Go back to main menu":
            main_menu()
    elif choice == "Analyze current habits":
        second_choice = questionary.select(
            "Choose option",
            choices=[
                "Analyze current longest streak for all habits per time period",
                "Analyze longest streak for a chosen habit",
                "Go back to main menu"
            ]
        ).ask()
        if second_choice == "Analyze current longest " \
                            "streak for all habits per time period":
            analyze.analyze_current_streak_max(time_period="d")
            analyze.analyze_current_streak_max(time_period="w")
            main_menu()
        elif second_choice == "Analyze longest streak for a chosen habit":
            try:
                habits = db.get_all_habits()
            except ValueError:
                print("\nThere are no habits in the database yet.\n"
                      " Please add a habit first.\n")

                # get the name and ID of habit
            choices = [f"{habit[0]}: {habit[1]}" for habit in habits]  # habit[0] = ID, habit[1] = name

            choice = questionary.select("Choose the habit you want to analyze: ", choices=choices).ask()
            if not choice:
                return
            habit_ID = int(choice.split(":")[0])

            # function
            analyze.analyze_current_streak_max(habit_ID=habit_ID)
            main_menu()
        elif second_choice == "Go back to main menu":
            main_menu()
    elif choice == "Exit the program":
        print("Have a nice day, see u tomorrow!")
        exit()



def check_off_habit():
    """
    Allow the user to check off a habit for today's completion.
    :return:
    """
    # check if there are habits in the database
    try:
        habits = db.get_all_habits()
    except ValueError:
        print("\nThere are no habits in the database yet.\n"
              " Please add a habit first.\n")

    # get the name and ID of habit
    choices = [f"{habit[0]}: {habit[1]}" for habit in habits]  # habit[0] = ID, habit[1] = name

    choice = questionary.select("Choose the habit you want to check off: ", choices=choices).ask()
    if not choice:
        return
    habit_ID = int(choice.split(":")[0])
    habit_name = choice.split(":")[1].strip()

    # checking off the habit in the db
    db.check_off_habit_in_db(habit_ID)

    # update streak information in the db
    db.update_streak_in_db(habit_ID)

    # User feedback
    print(f"Habit '{habit_name}' has been checked off for today!")



def add_new_habit():
    """
    Create a new habit entry through user input.

    :return:
    """
    name = questionary.text("Enter the name of the new habit: ").ask()
    description = questionary.text("Enter the description of the new habit: ").ask()
    time_period = questionary.select("""How often do you want to repeat this habit? \n
            Enter "d" for a daily habit and "w" for a weekly habit.""", choices=["d", "w"]).ask()

    habit = Habit(name=name, description=description, time_period=time_period)
    habit.add_habit_object(name=name, description=description, time_period=time_period)
    print(f"Habit {habit} successfully created!")


def edit_existing_habit():
    """
    Allow the user to edit the name and description of an existing habit.

    :return:
    """
    try:
        habits = db.get_all_habits()
        if not habits:
            print("There are no habits in the database yet.")
            return
    except Exception as e:
        print("Failed to retrieve habits from the database:", e)
        return
    choices = [f"{habit[0]}: {habit[1]}" for habit in habits]  # habit[0] = ID, habit[1] = name
    choice = questionary.select("Select a habit to edit:", choices=choices).ask()
    habit_ID = int(choice.split(":")[0])
    old_habit_name = choice.split(":")[1].strip()

    # new information
    new_habit_name = questionary.text("Enter the new name of the existing habit: ").ask()
    new_habit_description = questionary.text("Enter the new description of the existing habit: ").ask()

    # Confirm before updating
    confirm = questionary.confirm(
        f"Do you want to update the habit '{old_habit_name}' to:\n"
        f"Name: {new_habit_name}\nDescription: {new_habit_description}"
    ).ask()

    if confirm:
        db.update_habit_info(habit_ID, new_habit_name, new_habit_description)
        print("Habit successfully updated.")
    else:
        print("Update cancelled.")


def delete_existing_habit():
    """
    Allow the user to delete an existing habit from the database.
    :return:
    """
    try:
        habits = db.get_all_habits()
        if not habits:
            print("There are no habits in the database yet.")
            return
    except Exception as e:
        print("Failed to retrieve habits from the database:", e)
        return

    choices = [f"{habit[0]}: {habit[1]}" for habit in habits]  # habit[0] = ID, habit[1] = name
    choice = questionary.select("Select a habit to delete:", choices=choices).ask()
    habit_ID = int(choice.split(":")[0])
    habit_name = choice.split(":")[1].strip()

    confirm = questionary.confirm(
        f"Are you sure u want to delete the habit '{habit_name}' (ID: {habit_ID})?"
    ).ask()
    if confirm:
        db.delete_habit_from_db(habit_ID)
        print(f"Habit '{habit_name}' (ID: {habit_ID}) has been successfully deleted.")
    else:
        print("Deletion cancelled.")


if __name__ == "__main__":
    """
    Entry point for the habit tracking application.

    This block ensures the database is initialized (tables are created if they don't exist)
    and starts the main menu for user interaction.
    """
    db.initialize_db()
    main_menu()

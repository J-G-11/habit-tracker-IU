# habit-tracker-IU
# Habit Tracker CLI App

This is a command-line interface (CLI) habit tracking application written in Python. 
It allows users to create, check off, edit, delete, and analyze habits, while keeping 
track of their current and longest streaks. The program uses `sqlite3` for persistent 
storage and `questionary` for an interactive terminal UI.

---

## Features

- Check off daily or weekly habits
- Add new habits with a name, description, and time period
- Edit existing habit names and descriptions
- Delete habits and all associated data
- Analyze the longest streaks for specific or all habits
- View all habits or filter by time period (daily or weekly)
- Intuitive CLI using the `questionary` library

---

## Installation & running the program

- **Language**: Python 3.7+  
- **Database**: SQLite (`sqlite3` module)  
- **CLI Library**: [`questionary`](https://github.com/tmbo/questionary)  

To install the project download the repository and navigate to the project directory.\
To run the project: Enter 'python main.py' in your terminal. 

---

## Project Structure

```bash
.
├── main.py             # CLI interface and user navigation
├── habit.py            # Habit class and database interactions
├── db.py               # SQLite database setup and queries
├── analyze.py          # Functions for analyzing habits and streaks
├── database.db         # SQLite database file (auto-generated)
├── README.md           # Project documentation
```

___
## Usage
Upon launching, you can:

- **Create a habit** → Provide a name, description, and select d (daily) or w (weekly) habit time period
- **Check off a habit** → Select from the list and log today's completion
- **Analyze** → View current and longest streaks
- **Edit or Delete** → Update or remove habits by selecting from a list

All actions update the underlying SQLite database automatically. \
Use your arrow keys to navigate through the main menu and press **ENTER** to select your choice.

___
## Habit Object Structure
Each habit object contains the following attributes:
- `habit_ID` (int): Unique identifier

- `habit_name` (str): Name of the habit

- `habit_description` (str): Brief description

- `habit_time_period` (str): 'd' for daily or 'w' for weekly

- `habit_date_created` (str): Creation date

- `habit_counter` (int): Current streak

- `habit_counter_max` (int): Longest streak

- `habit_completed` (bool): Whether completed today

___
## Datastructures tables
The SQLite database includes:
- `habit_info `: Stores habit static data

- `habit_log `: Tracks check-off dates

- `habit_streak `: Stores current and max streaks

___
## Author
J. G. 

___
## License
This project is licensed under the MIT License.


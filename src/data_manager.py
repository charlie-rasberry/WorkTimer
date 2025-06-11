import json
from datetime import date

# This will be overwritten by interval.py to ensure the correct path is used
DATA_FILE = "cycle_data.json"


def load_data():
    """ Loads cycle data from the JSON file. """
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    """ Saves the given data dictionary to the JSON file. """
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def add_task_entry(task_name, duration_seconds):
    """ Adds a new task with its duration to today's entry in the JSON file. """
    today_str = date.today().isoformat()
    data = load_data()

    tasks_or_count = data.get(today_str)

    if isinstance(tasks_or_count, int):
        print(f"Migrating old data for {today_str}...")
        day_tasks = [{"task": "Legacy Task", "duration": 0} for _ in range(tasks_or_count)]
    elif isinstance(tasks_or_count, list):
        day_tasks = tasks_or_count
    else:
        day_tasks = []

    new_task = {
        "task": task_name,
        "duration": duration_seconds
    }
    day_tasks.append(new_task)

    data[today_str] = day_tasks
    save_data(data)
    print(f"Added task '{task_name}' for {today_str}")
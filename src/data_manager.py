import json
from datetime import date

DATA_FILE = "cycle_data.json"


def load_data():
    """
    Loads cycle data from the JSON file.
    If the file doesn't exist, returns an empty dictionary.
    """
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle cases where the file doesn't exist, is empty, or corrupted
        return {}


def save_data(data):
    """
    Saves the given data dictionary to the JSON file.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def increment_today_cycle_count():
    """
    Increments the cycle count for the current day.
    Loads the data, updates the count for today, and saves it back.
    """
    today_str = date.today().isoformat()  # Gets date in "YYYY-MM-DD" format
    data = load_data()

    current_count = data.get(today_str, 0)
    data[today_str] = current_count + 1

    save_data(data)
    print(f"Cycle count for {today_str} updated to: {data[today_str]}")
import json
from enum import Enum
from datetime import datetime


def dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [dataclass_to_dict(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = dataclass_to_dict(value)
        return result
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj


def read_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def get_datetime_parsed(date_str, time_str):
    # Assuming current year
    current_year = datetime.now().year

    # Combining the date and time strings
    datetime_str = f"{date_str}-{current_year} {time_str}"

    # Converting to datetime object
    datetime_object = datetime.strptime(datetime_str, "%d-%B-%Y %H:%M")
    return datetime_object

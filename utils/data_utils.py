import re
import json
from enum import Enum
from typing import Any
from datetime import datetime, timedelta

from models.squad import Squad
from models.athlete import Athlete


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


def dict_to_object(dictionary: Any) -> Any:
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            dictionary[key] = dict_to_object(value)
        return type('DynamicObject', (object,), dictionary)()
    elif isinstance(dictionary, list):
        return [dict_to_object(item) for item in dictionary]
    else:
        return dictionary


def get_datetime_parsed(date_str, time_str):
    # Assuming current year
    current_year = datetime.now().year

    # Combining the date and time strings
    datetime_str = f"{date_str}-{current_year} {time_str}"

    # Converting to datetime object
    datetime_object = datetime.strptime(datetime_str, "%d-%B-%Y %H:%M")
    return datetime_object


def get_datetime_str(date_str, time_str):
    if not date_str:
        # Use the current date when date_str is None
        current_date_str = datetime.now().strftime("%Y-%m-%d")
        datetime_str = f"{current_date_str} {time_str}"
        return datetime_str

    if not time_str:
        # Use the current time when time_str is None
        current_time_str = datetime.now().strftime("%H:%M:%S")
        datetime_str = f"{date_str} {current_time_str}"
        return datetime_str

    datetime_str = f"{date_str} {time_str}"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(datetime_str, datetime_format)

    dt += timedelta(hours=5, minutes=30)
    return dt



def extract_number_from_string(input_string):
    numbers = re.findall(r'\d+', input_string)
    if numbers:
        return int(numbers[0])
    else:
        return None
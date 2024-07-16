import json
from enum import Enum
from typing import Any
from datetime import datetime

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
    datetime_str = f"{date_str} {time_str}"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(datetime_str, datetime_format)


def get_single_squads(match, area_id_map):
    contestant_a_id = match.contestant_a_id
    contestant_a_name = match.contestant_a_common_name
    contestant_a_nationality = match.contestant_a_nationality_area_name
    contestant_a_nationality_id = match.contestant_a_nationality_area_id

    contestant_b_id = match.contestant_b_id
    contestant_b_name = match.contestant_b_common_name
    contestant_b_nationality = match.contestant_b_nationality_area_name
    contestant_b_nationality_id = match.contestant_b_nationality_area_id

    if contestant_a_nationality not in area_id_map:
        area_id_map[contestant_a_nationality] = contestant_a_nationality_id
    else:
        if area_id_map[contestant_a_nationality] != contestant_a_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b_nationality not in area_id_map:
        area_id_map[contestant_b_nationality] = contestant_b_nationality_id
    else:
        if area_id_map[contestant_b_nationality] != contestant_b_nationality_id:
            print("Mismatch in nationality id")

    athlete_a = Athlete(id=contestant_a_id, name=contestant_a_name)
    athlete_b = Athlete(id=contestant_b_id, name=contestant_b_name)

    squad_a = Squad(id=contestant_a_nationality_id,
                    name=contestant_a_nationality,
                    size=1,
                    athletes=[athlete_a])

    squad_b = Squad(id=contestant_b_nationality_id,
                    name=contestant_b_nationality,
                    size=1,
                    athletes=[athlete_b])

    return squad_a, squad_b


def get_doubles_squads(match, area_id_map):
    contestant_a1_id = match.contestant_a1_id
    contestant_a1_name = match.contestant_a1_common_name
    contestant_a1_nationality = match.contestant_a1_nationality_area_name
    contestant_a1_nationality_id = match.contestant_a1_nationality_area_id

    contestant_a2_id = match.contestant_a2_id
    contestant_a2_name = match.contestant_a2_common_name
    contestant_a2_nationality = match.contestant_a2_nationality_area_name
    contestant_a2_nationality_id = match.contestant_a2_nationality_area_id

    contestant_b1_id = match.contestant_b1_id
    contestant_b1_name = match.contestant_b1_common_name
    contestant_b1_nationality = match.contestant_b1_nationality_area_name
    contestant_b1_nationality_id = match.contestant_b1_nationality_area_id

    contestant_b2_id = match.contestant_b2_id
    contestant_b2_name = match.contestant_b2_common_name
    contestant_b2_nationality = match.contestant_b2_nationality_area_name
    contestant_b2_nationality_id = match.contestant_b2_nationality_area_id

    if contestant_a1_name == "Ena Shibahara":
        contestant_a1_nationality = 'Japan'
        contestant_a1_nationality_id = '102'

    elif contestant_a2_name == "Ena Shibahara":
        contestant_a2_nationality = 'Japan'
        contestant_a2_nationality_id = '102'

    elif contestant_b1_name == "Ena Shibahara":
        contestant_b1_nationality = 'Japan'
        contestant_b1_nationality_id = '102'

    elif contestant_b2_name == "Ena Shibahara":
        contestant_b2_nationality = 'Japan'
        contestant_b2_nationality_id = '102'

    if contestant_a1_nationality_id != contestant_a2_nationality_id:
        print("Error in Doubles Type Match")

    if contestant_a1_nationality not in area_id_map:
        area_id_map[contestant_a1_nationality] = contestant_a1_nationality_id
    else:
        if area_id_map[contestant_a1_nationality] != contestant_a1_nationality_id:
            print("Mismatch in nationality id")

    if contestant_a2_nationality not in area_id_map:
        area_id_map[contestant_a2_nationality] = contestant_a2_nationality_id
    else:
        if area_id_map[contestant_a2_nationality] != contestant_a2_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b1_nationality_id != contestant_b2_nationality_id:
        print("Error in Doubles Type Match")

    if contestant_b1_nationality not in area_id_map:
        area_id_map[contestant_b1_nationality] = contestant_b1_nationality_id
    else:
        if area_id_map[contestant_b1_nationality] != contestant_b1_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b2_nationality not in area_id_map:
        area_id_map[contestant_b2_nationality] = contestant_b2_nationality_id
    else:
        if area_id_map[contestant_b2_nationality] != contestant_b2_nationality_id:
            print("Mismatch in nationality id")

    athlete_a1 = Athlete(id=contestant_a1_id, name=contestant_a1_name)
    athlete_a2 = Athlete(id=contestant_a2_id, name=contestant_a2_name)
    athlete_b1 = Athlete(id=contestant_b1_id, name=contestant_b1_name)
    athlete_b2 = Athlete(id=contestant_b2_id, name=contestant_b2_name)

    squad_a = Squad(id=contestant_a1_nationality_id,
                    name=contestant_a1_nationality,
                    size=2,
                    athletes=[athlete_a1, athlete_a2])

    squad_b = Squad(id=contestant_b1_nationality_id,
                    name=contestant_b1_nationality,
                    size=2,
                    athletes=[athlete_b1, athlete_b2])

    return squad_a, squad_b


def get_team_squads(match, area_id_map):
    team_a_id = match.team_a_id
    team_a_name = match.team_a_area_name
    team_a_country_id = match.team_a_area_id

    team_b_id = match.team_b_area_id
    team_b_name = match.team_b_area_name
    team_b_country_id = match.team_b_area_id

    if team_a_name not in area_id_map:
        area_id_map[team_a_name] = team_a_country_id
    else:
        if area_id_map[team_a_name] != team_a_country_id:
            print("Mismatch in nationality id")

    if team_b_name not in area_id_map:
        area_id_map[team_b_name] = team_b_country_id
    else:
        if area_id_map[team_b_name] != team_b_country_id:
            print("Mismatch in nationality id")

    squad_a = Squad(id=team_a_country_id,
                    name=team_a_name)

    squad_b = Squad(id=team_b_country_id,
                    name=team_b_name)

    return squad_a, squad_b


def get_lineup_squad(lineup):
    nationalities = set()
    for player in lineup:
        nationalities.add(player.nationality)

    if len(nationalities) != 2:
        print("Error in Lineup")
        raise ValueError("Lineup Error")

    team_a = lineup.filter(lambda x: x.nationality == nationalities[0])
    team_b = lineup.filter(lambda x: x.nationality == nationalities[1])

    squad_a = Squad(id = team_a[0].nationality_area_id,
                    name = team_a[0].nationality,
                    size = len(team_a),
                    athletes = [])

    squad_b = Squad(id = team_b[0].nationality_area_id,
                    name = team_b[0].nationality,
                    size = len(team_b),
                    athletes = [])

    for player in team_a:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position,
                          shirt_number = player.shirtnumber)
        squad_a.athletes.append(athlete)

    for player in team_b:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position,
                          shirt_number = player.shirtnumber)
        squad_b.athletes.append(athlete)









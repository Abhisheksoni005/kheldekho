import requests

from models.event import Event
from models.sport import Sport
from collections import defaultdict
from requests.auth import HTTPBasicAuth
from utils.data_utils import dict_to_object

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


# Get list of all sports with disciplines
def get_all_sports_list():
    sport_api = BASE_API_URL + f"{username}/multisport/get_disciplines?&id={PARIS_ID}&client={username}&authkey={AUTH_KEY}&ftype=json"

    sport_response = requests.get(sport_api,
                                  auth=HTTPBasicAuth(username, password)
                                  )

    response_json = sport_response.json()
    sports = dict_to_object(response_json)

    sports_list = sports.datasportsgroup.sport

    sport_response = defaultdict(list)
    for sport_obj in sports_list:
        sport = sport_obj.sport

        obj_discipline = sport_obj.discipline
        if not isinstance(obj_discipline, list):
            print("Discipline is not a list, casting it to list")
            obj_discipline = [obj_discipline]

        for discipline in obj_discipline:
            sport_obj = Sport(id=discipline.discipline_id,
                              name=discipline.name,
                              type=discipline.type)

            sport_response[sport].append(sport_obj.to_json())

    return sport_response


# TODO: check gender here - api is not returning gender for these disciplines
def get_events_for_sport_list(sport_name):
    sport_api = BASE_API_URL + f"{username}/multisport/get_disciplines?&id={PARIS_ID}&client={username}&authkey={AUTH_KEY}&ftype=json"

    sport_response = requests.get(sport_api,
                                  auth=HTTPBasicAuth(username, password)
                                  )

    response_json = sport_response.json()
    sports = dict_to_object(response_json)

    sports_list = sports.datasportsgroup.sport

    for sport_obj in sports_list:
        if sport_obj.sport != sport_name:
            continue

        obj_discipline = sport_obj.discipline
        if not isinstance(obj_discipline, list):
            print("Discipline is not a list, casting it to list")
            obj_discipline = [obj_discipline]

        for discipline in obj_discipline:
            event_obj = Event(id=discipline.discipline_id,
                              name=discipline.name,
                              type=discipline.type,
                              parent_sport=sport_name)

            return event_obj


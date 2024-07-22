import requests
from requests.auth import HTTPBasicAuth

from models.athlete import Athlete
from utils.data_utils import dict_to_object

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


# def get_athlete_by_sport(sport_name, discipline_id: str = None):
#     athlete_api = BASE_API_URL + f"{username}/multisport/get_contestants?&id={TOKYO_ID}&client={username}&authkey={AUTH_KEY}&type=sport&type_id={sport_name}&ftype=json"
#
#     if discipline_id:
#         athlete_api += f"&discipline_id={discipline_id}"
#
#     athlete_response = requests.get(athlete_api,
#                                      auth=HTTPBasicAuth(username, password)
#                                      )
#
#     response_json = athlete_response.json()
#     athletes = dict_to_object(response_json)
#
#     events_list = athletes.datasportsgroup.multisport_event.multisport_event_season.sport
#
#     sport_name = events_list.name
#     events = events_list.discipline
#
#     for event in events:
#         event_id = event.id
#         event_name = event.name
#
#         for contest in event.gender:
#             gender = contest.value
#
#             for athlete in contest.contestant:
#                 athlete_id = athlete.people_id
#                 athlete_name = athlete.first_name + " " + athlete.last_name
#                 country = athlete.nationality_area_name
#                 country_id = athlete.nationality_area_id

# TODO: Add team event players here
def get_athletes_data(olympics_id, country_id):

    api_url = f"{BASE_API_URL}samarth/multisport/get_contestants?client={username}&authkey={AUTH_KEY}&type=area&type_id={country_id}&id={olympics_id}&ftype=json"

    athlete_response = requests.get(api_url,
                                    auth=HTTPBasicAuth(username, password))

    response_json = athlete_response.json()
    athletes = dict_to_object(response_json)

    sport_list = athletes.datasportsgroup.multisport_event.multisport_event_season.sport

    athlete_list = []
    for sport in sport_list:
        sport_discipline = sport.discipline
        if not isinstance(sport_discipline, list):
            sport_discipline = [sport_discipline]

        sport_name = sport.value
        for discipline in sport_discipline:
            discipline_gender = discipline.gender

            event_name = discipline.name

            if not isinstance(discipline_gender, list):
                discipline_gender = [discipline_gender]

                for gender_event in discipline_gender:
                    if not hasattr(gender_event, "contestant"):
                        continue
                    contestant_list = gender_event.contestant
                    if not isinstance(contestant_list, list):
                        contestant_list = [contestant_list]
                    for athlete in contestant_list:
                        athlete_id = athlete.people_id
                        athlete_name = athlete.common_name
                        country = athlete.nationality_area_name
                        country_flag = athlete.nationality_area_code

                        athlete = Athlete(id=athlete_id,
                                          name=athlete_name,
                                          country=country,
                                          country_code=country_flag,
                                          sport=sport_name,
                                          event=event_name)

                        athlete_list.append(athlete.to_json())

    return athlete_list




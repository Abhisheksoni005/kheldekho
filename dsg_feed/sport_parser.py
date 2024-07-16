import requests
from requests.auth import HTTPBasicAuth
from utils.data_utils import dict_to_object

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


athlete_api = BASE_API_URL + f"{username}/multisport/get_contestants?&id={PARIS_ID}&client={username}&authkey={AUTH_KEY}&type=sport&type_id=athletics&ftype=json"

athlete_response = requests.get(athlete_api,
                                 auth=HTTPBasicAuth(username, password)
                                 )

response_json = athlete_response.json()
athletes = dict_to_object(response_json)

events_list = athletes.datasportsgroup.multisport_event.multisport_event_season.sport

sport_name = events_list.name
events = events_list.discipline

for event in events:
    event_id = event.id
    event_name = event.name

    for contest in event.gender:
        gender = contest.value

        for athlete in contest.contestant:
            athlete_id = athlete.people_id
            athlete_name = athlete.first_name + " " + athlete.last_name
            country = athlete.nationality_area_name
            country_id = athlete.nationality_area_id



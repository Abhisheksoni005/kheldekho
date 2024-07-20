import requests
from requests.auth import HTTPBasicAuth

from dsg_feed.event_parser.athletics import get_field_event_details, get_marathon_details
from dsg_feed.event_parser.field_hockey import get_hockey_details
from utils.data_utils import dict_to_object, read_from_json

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"

area_id_map = read_from_json("dataset/country_id_map.json")


sport_list = ['archery', 'artistic_swimming', 'athletics', 'badminton', 'baseball', 'basketball',
              'boxing', 'breaking', 'canoeing', 'cycling', 'diving', 'equestrian', 'fencing',
              'field_hockey', 'golf', 'gymnastics', 'handball', 'judo', 'karate', 'modern_pentathlon',
              'rowing', 'rugby', 'sailing', 'shooting', 'skateboarding', 'soccer', 'sport_climbing',
              'surfing', 'swimming', 'table_tennis', 'taekwondo', 'tennis', 'triathlon', 'volleyball',
              'water_polo', 'weightlifting', 'wrestling']




f_type = "json"
# result_url = 'https://dsg-api.com/clients/samarth/badminton/get_matches?id=3337130&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'

url_dict = {
# "volleyball_url" : "https://dsg-api.com/clients/samarth/volleyball/get_matches?id=1875029&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "beach_volleyball_url" : "https://dsg-api.com/clients/samarth/volleyball/get_matches?id=2531294&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "badminton_singles_url" : "https://dsg-api.com/clients/samarth/badminton/get_matches?id=2522582&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "tennis_doubles_url" : "https://dsg-api.com/clients/samarth/tennis/get_matches?id=2600874&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "tennis_doubles_url1" : "https://dsg-api.com/clients/samarth/tennis/get_matches?id=3397334&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "marathon_api" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=54448&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "javelin_api" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=54414&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "high_jump" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=55358&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "relay_4x400" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=55591&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "discuss" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=55398&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "hurdle_110m" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=55493&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "pole_vault" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=55400&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
# "triple_jump" : "https://dsg-api.com/clients/samarth/athletics/get_results?id=54396&type=round&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth",
"field_hockey" : "https://dsg-api.com/clients/samarth/field_hockey/get_matches?id=2352005&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "soccer" : "https://dsg-api.com/clients/samarth/soccer/get_matches?id=2365900&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes"
}


field_event_list = ["High Jump",
                    "Javelin Throw",
                    "Discuss Throw",
                    "Triple Jump",
                    "Pole Vault"]


def parse_match(sport, event_name, event):
    details = None
    if sport == "athletics":
        if event_name in field_event_list:
            details = get_field_event_details(sport, event)

        if event_name == "Marathon":
            details = get_marathon_details(sport, event)

        if event_name == "4x400 Metres Relay":
            details = get_marathon_details(sport, event)

    if sport == "field_hockey":
        details = get_hockey_details(sport, event)

    return details


def get_match_details(sport_name, result_url):
    print(sport_name)
    result_url += f"&ftype={f_type}"

    result_response = requests.get(result_url,
                                   auth=HTTPBasicAuth(username, password)
                                   )

    result_json = result_response.json()
    result = dict_to_object(result_json)

    #start parsing
    sport = result.datasportsgroup.sport
    event = result.datasportsgroup.tour.tour_season.competition.season.discipline

    event_name = event.name
    gender = event.gender.value
    print(sport, event_name, gender)

    event_details = parse_match(sport, event_name, event)
    return event_details

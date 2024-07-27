import requests
from requests.auth import HTTPBasicAuth

from utils.data_utils import dict_to_object
from dsg_feed.event_parser.knockout_parser import parse_knockouts
from dsg_feed.event_parser.field_sports import get_team_match_details
from dsg_feed.event_parser.racquet_sports import get_racquet_sport_details
from dsg_feed.event_parser.athletics import get_field_event_details, get_marathon_details, get_relay4x400_details, \
    get_archery_recurve_details, get_archery_recurve_team_details

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


sport_list = ['archery', 'artistic_swimming', 'athletics', 'badminton', 'baseball', 'basketball',
              'boxing', 'breaking', 'canoeing', 'cycling', 'diving', 'equestrian', 'fencing',
              'field_hockey', 'golf', 'gymnastics', 'handball', 'judo', 'karate', 'modern_pentathlon',
              'rowing', 'rugby', 'sailing', 'shooting', 'skateboarding', 'soccer', 'sport_climbing',
              'surfing', 'swimming', 'table_tennis', 'taekwondo', 'tennis', 'triathlon', 'volleyball',
              'water_polo', 'weightlifting', 'wrestling']




f_type = "json"
# result_url = 'https://dsg-api.com/clients/samarth/badminton/get_matches?id=3337130&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'

url_dict = {
"volleyball_url" : "https://dsg-api.com/clients/samarth/volleyball/get_matches?id=1875029&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
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
# "field_hockey" : "https://dsg-api.com/clients/samarth/field_hockey/get_matches?id=2352005&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes",
# "soccer" : "https://dsg-api.com/clients/samarth/soccer/get_matches?id=2365900&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes"
}


field_event_list = ["High Jump",
                    "Javelin Throw",
                    "Discus Throw",
                    "Triple Jump",
                    "Pole Vault"]

track_event_list = ["100 Metres",
                    "110 Metres Hurdles",
                    "Marathon",
                    "10,000 Metres"]

racquet_sport_list = ["badminton",
                      "tennis",
                      "table_tennis",
                      "karate",
                      "boxing"]

racquet_event_list = ["Beach Volleyball", "Archery Team", "Recurve Team"]

team_sports = ["soccer",
               "field_hockey",
               "volleyball",
               "handball",
               "rugby",
               ]


def parse_match(sport, event_name, event, season_id):
    details = None
    if sport in ["athletics", "archery"]:
        if event_name in field_event_list:
            details = get_field_event_details(sport, event)

        if event_name in track_event_list:
            details = get_marathon_details(sport, event)

        if event_name == "4x400 Metres Relay":
            details = get_relay4x400_details(sport, event)

        if event_name in ["Recurve", "Archery"]:
            details = get_archery_recurve_details(sport, event)

        if event_name in ["Recurve Team", "Archery Team"]:
            details = get_archery_recurve_team_details(sport, event)

    elif sport in racquet_sport_list or event_name in racquet_event_list:
        details = get_racquet_sport_details(sport, event)

    elif sport in team_sports:
        details = get_team_match_details(sport, event)

    if details:
        details.season_id = season_id

    return details.to_json()


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
    season = result.datasportsgroup.tour.tour_season.competition.season

    event = season.discipline
    season_id = season.season_id
    event_name = event.name
    gender = event.gender.value
    print(sport, event_name, gender)

    event_details = parse_match(sport, event_name, event, season_id)
    return event_details


results_sports = ["athletics", "archery", "artistic_swimming", "breaking", "canoeing", "cycling", "diving", "equestrian",
                  "golf",  "gymnastics", "modern_pentathlon", "rowing", "sailing", "shooting", "skateboarding",
                  "surfing", "swimming", "triathlon", "weightlifting"]


def get_knockout_details(sport_name, event_name, season_id, gender):
    if sport_name in results_sports:
        api_name = "get_results"
    else:
        api_name = "get_matches"

    url = f"{BASE_API_URL}{username}/{sport_name}/{api_name}?type=season&id={season_id}&authkey={AUTH_KEY}&client={username}"

    # url = "https://dsg-api.com/clients/samarth/soccer/get_matches?type=season&id=49681&client=samarth&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"
    url += f"&ftype={f_type}"

    result_response = requests.get(url,
                                   auth=HTTPBasicAuth(username, password)
                                   )

    result_json = result_response.json()
    result = dict_to_object(result_json)

    discipline = result.datasportsgroup.tour.tour_season.competition.season.discipline

    if not isinstance(discipline, list):
        discipline = [discipline]

    gender_obj = None
    for event in discipline:
        if event.name == event_name:
            gender_obj = event.gender
            break

    if not gender_obj:
        print("Event not found")
        return []

    if not isinstance(gender_obj, list):
        gender_obj = [gender_obj]

    rounds = None
    for gender_type in gender_obj:
        if gender_type.value == gender:
            rounds = gender_type.round
            break

    if not rounds:
        print("Gender not found")
        return []

    knockout_details = parse_knockouts(sport_name, event_name, rounds, gender)
    return knockout_details

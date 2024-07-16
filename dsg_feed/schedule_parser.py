import requests
from requests.auth import HTTPBasicAuth

from models.athlete import Athlete
from models.match_multi import MatchMulti
from models.match_single import MatchSingle
from models.squad import Squad
from utils.data_utils import dict_to_object, get_datetime_str, read_from_json, get_team_squads, get_single_squads, \
    get_doubles_squads

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"

area_id_map = read_from_json("dataset/country_id_map.json")


def check_is_live(match_status: str):
    return match_status == "Playing"


def check_match_done(match_status: str):
    return match_status == "Played"


def get_event_name(gender, event):
    if gender == "male":
        return f"Men's {event}"
    elif gender == "female":
        return f"Women's {event}"
    else:
        return event


def get_schedule_matches(day: str = "2024-07-24"):
    calendar_api = BASE_API_URL + f"{username}/multisport/get_calendar?id={TOKYO_ID}&client={username}&authkey={AUTH_KEY}&ftype=json"
    # calendar_api = BASE_API_URL + f"{username}/multisport/get_calendar?id={PARIS_ID}&client={username}&authkey={AUTH_KEY}&day={day}&ftype=json"
    schedule_response = requests.get(calendar_api, auth=HTTPBasicAuth(username, password))

    schedule_response_json = schedule_response.json()
    schedule_obj = dict_to_object(schedule_response_json)

    matches_list = schedule_obj.datasportsgroup.multisport_event.multisport_event_season.day
    area_id_map = {}

    date = matches_list.date
    rounds = matches_list.rounds

    if not isinstance(rounds, list):
        print(date)
        print("Rounds is not a list, casting it to list")
        rounds = [rounds]

    response = []
    try:
        for sport_round_index, sport_round in enumerate(rounds):
            sport_name = sport_round.sport
            gender = sport_round.gender
            match_stage = sport_round.name
            event = sport_round.discipline_name
            event_id = sport_round.discipline_id
            medal_round = sport_round.medal_round

            calendar_type = sport_round.calendar_type

            try:

                # Signifies MatchSingle
                if calendar_type == "matches":

                    # Decided matches
                    if hasattr(sport_round, "match"):
                        if not isinstance(sport_round.match, list):
                            print("Match is not a list, casting it to list")
                            sport_round.match = [sport_round.match]

                        for match in sport_round.match:
                            match_id = match.match_id
                            status = match.status
                            time_utc = match.time_utc
                            result_url = match.result

                            squad_a = None
                            squad_b = None

                            # Doubles Type match
                            if hasattr(match, "contestant_a1_common_name"):
                                squad_a, squad_b = get_doubles_squads(match, area_id_map)

                            # Singles Type match
                            elif hasattr(match, "contestant_a_common_name"):
                                squad_a, squad_b = get_single_squads(match, area_id_map)

                            # Team A vs Team B Type match
                            elif hasattr(match, "team_a_name"):
                                squad_a, squad_b = get_team_squads(match, area_id_map)

                            # Call match object
                            match_single = MatchSingle(id=match_id,
                                                       sport=sport_name,
                                                       gender=gender,
                                                       event=get_event_name(gender, event),
                                                       event_id=event_id,
                                                       timestamp=get_datetime_str(date, time_utc),
                                                       is_live=check_is_live(status),
                                                       notification=False,
                                                       match_done=check_match_done(status),
                                                       stage=match_stage,
                                                       medal_round=medal_round,
                                                       team_a=squad_a,
                                                       team_b=squad_b,
                                                       result_url=result_url
                                                       )

                            response.append(match_single)

                    # Scheduled matches (Players not decided)
                    else:
                        status = sport_round.status
                        time_utc = sport_round.start_time_utc

                        # Call Match Object
                        match_single = MatchSingle(sport=sport_name,
                                                   gender=gender,
                                                   event=get_event_name(gender, event),
                                                   event_id=event_id,
                                                   timestamp=get_datetime_str(date, time_utc),
                                                   is_live=check_is_live(status),
                                                   stage=match_stage,
                                                   notification=False,
                                                   match_done=check_match_done(status),
                                                   medal_round=medal_round)

                        response.append(match_single)

                # Signifies MatchMulti
                else:
                    round_id = sport_round.round_id
                    status = sport_round.status
                    time_utc = sport_round.start_time_utc
                    winner_name = sport_round.winner_common_name
                    winner_nationality = sport_round.winner_nationality_area_name
                    winner_nationality_id = sport_round.winner_nationality_area_id

                    result_url = sport_round.result

                    ranking_dict = {
                        "1" : {
                            "winner": winner_name,
                            "winner_country": winner_nationality,
                            "winner_country_id": winner_nationality_id
                        }
                    }

                    # Call Match Object
                    match_multi = MatchMulti(id=round_id,
                                             sport=sport_name,
                                             gender=gender,
                                             event=get_event_name(gender, event),
                                             timestamp=get_datetime_str(date, time_utc),
                                             stage=match_stage,
                                             is_live=check_is_live(status),
                                             medal_round=medal_round,
                                             result_url=result_url,
                                             ranking=ranking_dict)

                    response.append(match_multi)

            except Exception as e:
                print(e)
                print(sport_round_index, sport_name)
                print("Error processing event")

        return response

    except Exception as e:
        print(e)
        print("Error processing Round")







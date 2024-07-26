import traceback

import requests
from requests.auth import HTTPBasicAuth

from dsg_feed.event_parser.common_parser import get_doubles_squads, get_single_squads, get_team_squads, get_country_code
from models.match_multi import MatchMulti
from models.match_single import MatchSingle
from utils.data_utils import dict_to_object, get_datetime_str, read_from_json

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


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


def filter_out_match_for_player(player_id, squad_a, squad_b):
    if not player_id:
        return False

    for player in squad_a.athletes:
        if player_id == player.id:
            return False

    for player in squad_b.athletes:
        if player_id == player.id:
            return False

    return True


results_sports = ["athletics", "archery", "artistic_swimming", "breaking", "canoeing", "cycling", "diving", "equestrian",
                  "golf",  "gymnastics", "modern_pentathlon", "rowing", "sailing", "shooting", "skateboarding",
                  "surfing", "swimming", "triathlon", "weightlifting"]


def has_india(match_obj):
    if "team_a" in match_obj and match_obj["team_a"]["flag"] == "IND" or "team_b" in match_obj and match_obj["team_b"]["flag"] == "IND":
        return True
    elif "ranking_dict" in match_obj and match_obj.ranking_dict.get("1").get("winner_country_code") == "IND":
        return True


def get_schedule_matches(day: str = None, sport_name: str = None, discipline_id: str = None, olympics_id: str = PARIS_ID, player_id: str = None):
    calendar_api = BASE_API_URL + f"{username}/multisport/get_calendar?id={olympics_id}&client={username}&authkey={AUTH_KEY}&ftype=json"

    if day:
        calendar_api += f"&day={day}"
    if sport_name:
        calendar_api += f"&sport={sport_name}"
        if discipline_id:
            calendar_api += f"&discipline_id={discipline_id}"

    print(calendar_api)

    schedule_response = requests.get(calendar_api, auth=HTTPBasicAuth(username, password))

    schedule_response_json = schedule_response.json()
    schedule_obj = dict_to_object(schedule_response_json)

    season = schedule_obj.datasportsgroup.multisport_event.multisport_event_season
    if not hasattr(season, "day"):
        print("Day attribute not found")
        return []

    rounds = []
    if day is None:
        date = None
        for day in season.day:
            matches_list = day
            list_rounds = matches_list.rounds
            if not isinstance(list_rounds, list):
                print("Rounds is not a list, casting it to list")
                list_rounds = [list_rounds]
            rounds += list_rounds
    else:
        matches_list = season.day
        date = matches_list.date
        rounds = matches_list.rounds

    if not isinstance(rounds, list):
        print("Date: ", date)
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
                            winner = ""
                            if hasattr(match, "winner"):
                                winner = match.winner

                            squad_a = None
                            squad_b = None

                            # Doubles Type match
                            if hasattr(match, "contestant_a1_common_name"):
                                squad_a, squad_b = get_doubles_squads(match)

                            # Singles Type match
                            elif hasattr(match, "contestant_a_common_name"):
                                squad_a, squad_b = get_single_squads(match)

                            # Team A vs Team B Type match
                            elif hasattr(match, "team_a_name"):
                                squad_a, squad_b = get_team_squads(match)

                            if filter_out_match_for_player(player_id, squad_a, squad_b):
                                continue

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

                            response.append(match_single.to_json())

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

                        response.append(match_single.to_json())

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
                            "winner_country_id": winner_nationality_id,
                            "winner_country_code": get_country_code(winner_nationality_id)
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

                    response.append(match_multi.to_json())

            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print(sport_round_index, sport_name)
                print("Error processing event")

        sorted_response = sorted(response,
                                 key=lambda x: (0 if has_india(x) else 1,
                                                0 if x["is_live"] else 1,
                                                x["timestamp"])
                                 )
        return sorted_response

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("Error processing Round")








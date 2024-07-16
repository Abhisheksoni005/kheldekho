import requests
from requests.auth import HTTPBasicAuth

from models.squad import Squad
from models.athlete import Athlete
from utils.data_utils import dict_to_object, read_from_json, get_doubles_squads, get_single_squads, get_lineup_squad

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"

area_id_map = read_from_json("dataset/country_id_map.json")

f_type = "json"
# result_url = 'https://dsg-api.com/clients/samarth/badminton/get_matches?id=3337130&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'

volleyball_url = 'https://dsg-api.com/clients/samarth/volleyball/get_matches?id=1875029&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'
# beach_volleyball_url = 'https://dsg-api.com/clients/samarth/volleyball/get_matches?id=2531294&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'
# badminton_singles_url = 'https://dsg-api.com/clients/samarth/badminton/get_matches?id=2522582&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'
# tennis_doubles_url = 'https://dsg-api.com/clients/samarth/tennis/get_matches?id=2600874&type=match&authkey=VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh&client=samarth&detailed=yes'


# parsing badminton singles
result_url = volleyball_url
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

match_round = event.gender.round

stage = match_round.name
match = match_round.list.match

if hasattr(match, "contestant_a1_common_name"):
    squad_a, squad_b = get_doubles_squads(match, area_id_map)

elif hasattr(match, "contestant_a_common_name"):
    squad_a, squad_b = get_single_squads(match, area_id_map)

elif hasattr(match, "events"):
    squad_a, squad_b = get_lineup_squad(match.events.lineups.event)
    coach_a, coach_b = get_lineup_squad(match.events.coaches.event)
    substitute_a, substitute_b = get_lineup_squad(match.events.subs_on_bench.event)

sets = []
for set_number, game in enumerate(match.period_scores.period):
    set_num = set_number
    game_score_a = game.score_a
    game_score_b = game.score_b

    sets.append({
        "set_num": set_num,
        "set_score_a": game_score_a,
        "set_score_b": game_score_b,
    })

set_score_a = match.score_a
set_score_b = match.score_b
status = match.status
time_utc = match.time_utc
winner = match.winner














def parse_json(data):
    datasportsgroup = data.get('datasportsgroup', {})
    print(f"Version: {datasportsgroup.get('version')}")
    print(f"Sport: {datasportsgroup.get('sport')}")

    method = datasportsgroup.get('method', {})
    print(f"Method ID: {method.get('method_id')}, Name: {method.get('name')}")

    tour = datasportsgroup.get('tour', {})
    print(f"Tour ID: {tour.get('tour_id')}, Name: {tour.get('name')}, Gender: {tour.get('gender')}")

    tour_season = tour.get('tour_season', {})
    print(f"Tour Season ID: {tour_season.get('tour_season_id')}, Title: {tour_season.get('title')}")

    tournament = tour_season.get('tournament', {})
    print(f"Tournament ID: {tournament.get('tournament_id')}, Name: {tournament.get('tournament_name')}")
    print(f"Area ID: {tournament.get('area_id')}, Name: {tournament.get('area_name')}")
    print(
        f"Season ID: {tournament.get('season_id')}, Title: {tournament.get('season_title')}, Name: {tournament.get('season_name')}")

    rounds = tournament.get('round', [])
    for round_ in rounds:
        print(
            f"Round ID: {round_.get('round_id')}, Name: {round_.get('name')}, Start Date: {round_.get('start_date')}, End Date: {round_.get('end_date')}")

        matches = round_.get('match', [])
        for match in matches:
            print(f"  Match ID: {match.get('match_id')}, Date: {match.get('date')}, Time: {match.get('time')}")
            print(
                f"    Contestant A: {match.get('contestant_a_first_name')} {match.get('contestant_a_last_name')}, Nationality: {match.get('contestant_a_nationality')}")
            print(
                f"    Contestant B: {match.get('contestant_b_first_name')} {match.get('contestant_b_last_name')}, Nationality: {match.get('contestant_b_nationality')}")
            print(f"    Winner: {match.get('winner')}, Status: {match.get('status')}")

            sets = match.get('set', [])
            if isinstance(sets, dict):  # single set case
                sets = [sets]
            for set_ in sets:
                print(
                    f"      Set {set_.get('num')}: Score A: {set_.get('score_a')}, Score B: {set_.get('score_b')}, Winner: {set_.get('winner')}")


# Load JSON data and parse it
# data = json.loads(json_data)
# parse_json(data)
from dsg_feed.event_parser.common_parser import get_doubles_squads, get_single_squads, get_team_squads
from dsg_feed.schedule_parser import check_is_live, check_match_done
from models.match_single import MatchSingle, Score
from utils.data_utils import get_datetime_str

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


def create_group_table(matches_list):
    teams = {}

    for match in matches_list:
        team_a = match.team_a.name
        team_b = match.team_b.name
        score_a = match.score.score_a
        score_b = match.score.score_b

        if team_a not in teams:
            teams[team_a] = {
                'country_name': team_a,
                'country_flag': match.team_a.flag,
                'matches_played': 0,
                'goals_scored': 0,
                'goals_against': 0,
                'GD': 0,
                'points': 0
            }

        if team_b not in teams:
            teams[team_b] = {
                'country_name': team_b,
                'country_flag': match.team_b.flag,
                'matches_played': 0,
                'goals_scored': 0,
                'goals_against': 0,
                'GD': 0,
                'points': 0
            }

        if score_a:
            teams[team_a]['matches_played'] += 1
            teams[team_b]['matches_played'] += 1

            teams[team_a]['goals_scored'] += score_a
            teams[team_b]['goals_scored'] += score_b

            teams[team_a]['goals_against'] += score_b
            teams[team_b]['goals_against'] += score_a

            teams[team_a]['GD'] += (score_a - score_b)
            teams[team_b]['GD'] += (score_b - score_a)

            if score_a > score_b:
                teams[team_a]['points'] += 3
            elif score_b > score_a:
                teams[team_b]['points'] += 3
            else:
                teams[team_a]['points'] += 1
                teams[team_b]['points'] += 1

    team_stats = list(teams.values())
    sorted_team_stats = sorted(team_stats, key=lambda x: x['points'], reverse=True)
    final_table = []
    for team in sorted_team_stats:
        if team['country_name'] == 'TBD':
            continue
        final_table.append({
            'country_name': team['country_name'],
            'country_flag': team['country_flag'],
            'metadata' :
                {
                    'Played': team['matches_played'],
                    'Points': team['points'],
                    'GD': team['GD'],

                }
        })

    return final_table


def parse_knockouts(sport_name, event_name, rounds, gender):
    groups = []
    knockouts = []

    for match_round in rounds:
        round_name = match_round.name
        matches = match_round.list

        if round_name in ["Group Stage", "Elimination Round"]:
            for group in matches:
                group_name = group.name
                group_matches = group.match
                group_matches_list = []
                for group_match in group_matches:
                    group_match_id = group_match.match_id
                    group_match_status = group_match.status
                    group_match_time_utc = group_match.time_utc
                    group_match_date = group_match.date_utc
                    group_match_winner = group_match.winner

                    squad_a = None
                    squad_b = None

                    group_result_url = f"{BASE_API_URL}{username}/{sport_name}/get_matches?type=match&id={group_match_id}&authkey={AUTH_KEY}&client={username}&detailed=yes"

                    # Doubles Type match
                    if hasattr(group_match, "contestant_a1_common_name"):
                        squad_a, squad_b = get_doubles_squads(group_match)

                    # Singles Type match
                    elif hasattr(group_match, "contestant_a_common_name"):
                        squad_a, squad_b = get_single_squads(group_match)

                    # Team A vs Team B Type match
                    elif hasattr(group_match, "team_a_name"):
                        squad_a, squad_b = get_team_squads(group_match)

                    status = group_match.status
                    score_a = group_match.score_a
                    score_b = group_match.score_b
                    if score_a == '':
                        score = Score()
                    else:
                        score = Score(score_a=int(score_a),
                                      score_b=int(score_b))

                    match_single = MatchSingle(id=group_match_id,
                                               sport=sport_name,
                                               gender=gender,
                                               event=event_name,

                                               timestamp=get_datetime_str(group_match_date, group_match_time_utc),
                                               is_live=check_is_live(group_match_status),
                                               notification=False,
                                               match_done=check_match_done(group_match_status),
                                               stage=round_name,
                                               winner=group_match_winner,
                                               status=status,

                                               team_a=squad_a,
                                               team_b=squad_b,
                                               score=score,
                                               result_url=group_result_url
                                               )

                    group_matches_list.append(match_single)

                group_table = create_group_table(group_matches_list)
                group_match = {"name": group_name,
                               "matches": group_table}
                groups.append(group_match)

        else:
            knockout_matches_list = []
            if not isinstance(matches.match, list):
                matches.match = [matches.match]
                print(f"Stage: {round_name} Match is not a list, casting it to list")
            for match in matches.match:
                match_id = match.match_id
                status = match.status

                time_utc = match.time_utc
                date = match.date_utc
                winner = match.winner

                squad_a = None
                squad_b = None

                result_url = f"{BASE_API_URL}{username}/{sport_name}/get_matches?type=match&id={match_id}&authkey={AUTH_KEY}&client={username}&detailed=yes"

                # Doubles Type match
                if hasattr(match, "contestant_a1_common_name"):
                    squad_a, squad_b = get_doubles_squads(match)

                # Singles Type match
                elif hasattr(match, "contestant_a_common_name"):
                    squad_a, squad_b = get_single_squads(match)

                # Team A vs Team B Type match
                elif hasattr(match, "team_a_name"):
                    squad_a, squad_b = get_team_squads(match)

                score_a = match.score_a
                score_b = match.score_b
                score = Score(score_a=int(score_a) if score_a != '' else 0,
                              score_b=int(score_b) if score_b != '' else 0)

                match_single = MatchSingle(id=match_id,
                                           sport=sport_name,
                                           gender=gender,
                                           event=event_name,

                                           timestamp=get_datetime_str(date, time_utc),
                                           is_live=check_is_live(status),
                                           notification=False,
                                           match_done=check_match_done(status),
                                           stage=round_name,
                                           winner=winner,

                                           team_a=squad_a,
                                           team_b=squad_b,
                                           score=score,
                                           result_url=result_url
                                           )

                knockout_matches_list.append(match_single.to_json())

            knockout_round = {"name": round_name,
                              "matches": knockout_matches_list}
            knockouts.append(knockout_round)

    return {"groups": groups, "knockouts": knockouts}















from dsg_feed.event_parser.common_parser import get_doubles_squads, get_single_squads, get_team_squads
from dsg_feed.schedule_parser import check_is_live, check_match_done
from models.match_single import MatchSingle
from utils.data_utils import get_datetime_str

BASE_API_URL = "https://dsg-api.com/clients/"
PARIS_ID = 72
TOKYO_ID = 1

username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"


def parse_knockouts(sport_name, event_name, rounds, gender):
    groups = {}
    knockouts = {}

    for match_round in rounds:
        round_name = match_round.name
        matches = match_round.list

        if round_name == "Group Stage":
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

                                               team_a=squad_a,
                                               team_b=squad_b,
                                               result_url=group_result_url
                                               )

                    group_matches_list.append(match_single.to_json())

                groups[group_name] = group_matches_list

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
                                           result_url=result_url
                                           )

                knockout_matches_list.append(match_single.to_json())

            knockouts[round_name] = knockout_matches_list

    return {"groups": groups, "knockouts": knockouts}















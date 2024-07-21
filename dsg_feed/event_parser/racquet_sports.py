from dsg_feed.event_parser.common_parser import update_squads, SetScore, update_team_details
from models.sport_models.RacquetSport import RacquetEvent, ScoreDetails
from utils.data_utils import get_datetime_str


def get_event_details(sport, event):
    match_round = event.gender.round
    group_name = match_round.list.name
    event_id = event.discipline_id
    gender = event.gender.value
    event_name = event.name
    notification = False
    stage = match_round.name

    match = match_round.list.match
    match_id = match.match_id
    time_utc = match.time_utc
    date = match.date_utc

    status = match.status
    winner = match.winner

    event_obj = RacquetEvent(sport=sport,
                             event=event_name,
                             event_id=event_id,
                             gender=gender,
                             event_name=event_name,
                             notification=notification,
                             stage=stage,
                             group_name=group_name,

                             match_id=match_id,
                             time_utc=get_datetime_str(date, time_utc),
                             winner=winner,
                             status=status)

    return event_obj


def update_score(match):
    if hasattr(match, "live") and hasattr(match.live, "game_minute"):
        game_time = match.live.game_minute
    else:
        game_time = ""

    sets = []
    for set_number, game in enumerate(match.period_scores.period):
        set_score = SetScore(set_num=set_number + 1,
                             match_score_a=game.score_a,
                             match_score_b=game.score_b)
        sets.append(set_score)

    score_details = ScoreDetails(score_a=match.score_a,
                                 score_b=match.score_b,
                                 game_time=game_time,
                                 sets=sets)
    return score_details


def get_racquet_sport_details(sport, event):
    badminton = get_event_details(sport, event)

    match = event.gender.round.list.match
    update_squads(match, badminton)
    update_team_details(match, badminton)
    badminton.score_details = update_score(match)

    return badminton.to_json()
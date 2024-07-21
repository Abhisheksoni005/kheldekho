from dsg_feed.event_parser.common_parser import get_lineup_squad, get_doubles_squads, get_single_squads
from models.sport_models.field_sports import TeamEvent, SetScore, ScoreDetails, Goals, Cards, Timeline
from utils.data_utils import extract_number_from_string


# TODO
# check list.name for badminton
# TODO
# check with support values of match.live - game_minute and period


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


def update_timeline(sport, match, team_a_id, team_b_id):

    if sport == "field_hockey":
        period_name_dict = {1 : "1st Quarter",
                            2 : "2nd Quarter",
                            3 : "3rd Quarter",
                            4 : "4th Quarter",
                            -1 : "Extra Time"}

    if sport == "soccer":
        period_name_dict = {1 : "1st Half",
                            2 : "2nd Half",
                            -1 : "Extra Time"}

    goal = match.events.scores
    card = match.events.bookings

    all_goals = []
    score_a = 0
    score_b = 0
    for goal in goal.event:
        goal_type = goal.type
        time = goal.minute
        extra_time = goal.minute_extra
        athlete_name = goal.common_name
        athlete_id = goal.people_id
        period = extract_number_from_string(goal.period)
        if not period:
            period = -1

        if goal.team_id == team_a_id:
            score_a += 1
        elif goal.team_id == team_b_id:
            score_b += 1

        new_goal = Goals(goal_type=goal_type,
                         time=time,
                         extra_time=extra_time,
                         athlete_name=athlete_name,
                         athlete_id=athlete_id,
                         score_a=str(score_a),
                         score_b=str(score_b),
                         period=period)

        all_goals.append(new_goal)

    all_cards = []
    for card in card.event:
        card_type = card.type
        time = card.minute
        extra_time = card.minute_extra
        athlete_name = card.common_name
        athlete_id = card.people_id
        country = card.nationality
        country_id = card.team_id
        period = extract_number_from_string(card.period)
        if not period:
            period = -1

        new_card = Cards(card_type=card_type,
                         time=time,
                         extra_time=extra_time,
                         athlete_name=athlete_name,
                         athlete_id=athlete_id,
                         country=country,
                         country_id=country_id,
                         period=period)

        all_cards.append(new_card)

    timeline_list = []

    for goal in all_goals:
        period_name = period_name_dict.get(goal.period)
        timeline_exists = False

        for timeline in timeline_list:
            if timeline.period_name == period_name:
                timeline.goals.append(goal)
                timeline_exists = True
                break

        if not timeline_exists:
            timeline = Timeline(period_name=period_name,
                                goals=[goal],
                                cards=[])
            timeline_list.append(timeline)
    
    for card in all_cards:
        period_name = period_name_dict.get(card.period)
        timeline_exists = False

        for timeline in timeline_list:
            if timeline.period_name == period_name:
                timeline.cards.append(card)
                timeline_exists = True
                break

        if not timeline_exists:
            timeline = Timeline(period_name=period_name,
                                goals=[],
                                cards=[card])
            timeline_list.append(timeline)

    return timeline_list


def get_field_match_details(sport, event):
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
    venue = match.match_extra.venue.venue_name

    team_a_id = match.team_a_id
    team_a_area_code = match.team_a_area_code
    team_a_area_name = match.team_a_area_name

    team_b_id = match.team_b_id
    team_b_area_code = match.team_b_area_code
    team_b_area_name = match.team_b_area_name
    winner = match.winner
    status = match.status

    teams_obj = TeamEvent(sport=sport,
                          event=event_name,
                          event_id=event_id,
                          gender=gender,
                          notification=notification,

                          match_id=match_id,
                          stage=stage,
                          group_name=group_name,
                          time_utc=time_utc,
                          venue=venue,
                          winner=winner,
                          status=status,

                          team_a_id=team_a_id,
                          team_a_name=team_a_area_name,
                          team_a_country=team_a_area_code,
                          team_b_id=team_b_id,
                          team_b_name=team_b_area_name,
                          team_b_country=team_b_area_code)

    return teams_obj


def update_squads(match, teams_obj):
    if hasattr(match, "contestant_a1_common_name"):
        squad_a, squad_b = get_doubles_squads(match)
        teams_obj.squad_a = squad_a
        teams_obj.squad_b = squad_b

    # Valid for badminton, tennis, beach volleyball
    elif hasattr(match, "contestant_a_common_name"):
        squad_a, squad_b = get_single_squads(match)
        teams_obj.squad_a = squad_a
        teams_obj.squad_b = squad_b

    # Valid for team events - hockey, football
    elif hasattr(match, "events"):
        squad_a, squad_b = get_lineup_squad(match.events.lineups.event, match.team_a_id, match.team_b_id)
        coach_a, coach_b = get_lineup_squad(match.events.coaches.event, match.team_a_id, match.team_b_id)
        substitute_a, substitute_b = get_lineup_squad(match.events.subs_on_bench.event, match.team_a_id, match.team_b_id)
        teams_obj.squad_a = squad_a
        teams_obj.squad_b = squad_b
        teams_obj.coach_a = coach_a
        teams_obj.coach_b = coach_b
        teams_obj.substitute_a = substitute_a
        teams_obj.substitute_b = substitute_b

    return teams_obj


def get_hockey_details(sport, event):
    hockey = get_field_match_details(sport, event)

    match = event.gender.round.list.match

    update_squads(match, hockey)
    hockey.score_details = update_score(match)
    hockey.timeline = update_timeline(sport, match, hockey.team_a_id, hockey.team_b_id)

    return hockey.to_json()

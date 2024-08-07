from dsg_feed.event_parser.common_parser import update_squads
from models.sport_models.field_sports import TeamEvent, SetScore, ScoreDetails, Goals, Cards, Timeline, MergedTimeline
from utils.data_utils import extract_number_from_string, get_datetime_str


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
    period = match.period_scores.period if hasattr(match.period_scores, "period") else []
    if not isinstance(period, list):
        period = [period]
    for set_number, game in enumerate(period):
        set_score = SetScore(set_num=set_number + 1,
                             match_score_a=game.score_a,
                             match_score_b=game.score_b)
        sets.append(set_score)

    score_details = ScoreDetails(score_a=match.score_a,
                                 score_b=match.score_b,
                                 game_time=game_time,
                                 sets=sets)
    return score_details


def merge_timeline_objects(timeline_list):
    merged_list = []
    for timeline_obj in timeline_list:
        period_name = timeline_obj.period_name
        events = []
        events.extend(timeline_obj.goals)
        events.extend(timeline_obj.cards)
        events.extend(timeline_obj.shootouts)

        events.sort(key=lambda x: (int(x.time.split('+')[0]), int(x.extra_time or 0)), reverse=True)

        timeline_dict = MergedTimeline(name=period_name,
                                       events=events)

        merged_list.append(timeline_dict)

    return merged_list


def update_timeline(sport, match, team_a_id, team_b_id):

    if sport == "volleyball":
        return []

    elif sport == "field_hockey":
        period_name_dict = {1 : "1st Quarter",
                            2 : "2nd Quarter",
                            3 : "3rd Quarter",
                            4 : "4th Quarter",
                            -1 : "Extra Time"}

    elif sport in ["soccer", "handball", "rugby"]:
        period_name_dict = {1 : "1st Half",
                            2 : "2nd Half",
                            -1 : "Extra Time"}

    goal = match.events.scores if hasattr(match.events, "scores") else []
    penalty = match.events.shootout if hasattr(match.events, "shootout") else []
    card = match.events.bookings if hasattr(match.events, "bookings") else []

    all_goals = []
    score_a = 0
    score_b = 0

    if hasattr(goal, "event"):
        if not isinstance(goal.event, list):
            goal.event = [goal.event]
        for goal in goal.event:
            goal_type = goal.type
            time = goal.minute
            extra_time = goal.minute_extra if hasattr(goal, "minute_extra") else ""
            athlete_name = goal.common_name
            athlete_id = goal.people_id
            period = extract_number_from_string(goal.period)
            if not period:
                period = -1

            team = ""
            if goal.team_id == team_a_id:
                score_a += 1
                team = "team_a"
            elif goal.team_id == team_b_id:
                score_b += 1
                team = "team_b"

            new_goal = Goals(goal_type=goal_type,
                             time=time,
                             extra_time=extra_time,
                             athlete_name=athlete_name,
                             athlete_id=athlete_id,
                             score_a=str(score_a),
                             score_b=str(score_b),
                             period=period,
                             team=team)

            all_goals.append(new_goal)

    shootouts = []
    pen_goal_a = 0
    pen_goal_b = 0
    if hasattr(penalty, "event"):
        if not isinstance(penalty.event, list):
            penalty.event = [penalty.event]
        for penalty in penalty.event:
            goal_type = penalty.type
            time = penalty.minute
            extra_time = penalty.minute_extra
            athlete_name = penalty.common_name
            athlete_id = penalty.people_id
            period = extract_number_from_string(penalty.period)
            if not period:
                period = -1

            team = ""
            if penalty.team_id == team_a_id:
                team = "team_a"
                if goal_type == "penalty_shootout_goal":
                    pen_goal_a += 1
            elif penalty.team_id == team_b_id:
                team = "team_b"
                if goal_type == "penalty_shootout_goal":
                    pen_goal_b += 1

            new_goal = Goals(goal_type=goal_type,
                             time=time,
                             extra_time=extra_time,
                             athlete_name=athlete_name,
                             athlete_id=athlete_id,
                             period=period,
                             score_a=str(pen_goal_a),
                             score_b=str(pen_goal_b),
                             team=team)

            shootouts.append(new_goal)

    all_cards = []
    if hasattr(card, "event"):
        if not isinstance(card.event, list):
            card.event = [card.event]
        for card in card.event:
            card_type = card.type
            time = card.minute
            extra_time = card.minute_extra if hasattr(card, "minute_extra") else ""
            athlete_name = card.common_name
            athlete_id = card.people_id
            country = card.nationality
            country_id = card.team_id
            period = extract_number_from_string(card.period)
            if not period:
                period = -1

            team = ""
            if card.team_id == team_a_id:
                team = "team_a"
            elif card.team_id == team_b_id:
                team = "team_b"

            new_card = Cards(card_type=card_type,
                             time=time,
                             extra_time=extra_time,
                             athlete_name=athlete_name,
                             athlete_id=athlete_id,
                             country=country,
                             country_id=country_id,
                             period=period,
                             team=team)

            all_cards.append(new_card)

    # TODO : add empty period if no event in the period
    timeline_list = []

    reversed_goals = all_goals[::-1]
    for goal in reversed_goals:
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
                                shootouts=[],
                                cards=[])
            timeline_list.append(timeline)

    reversed_pens = shootouts[::-1]
    for shootout in reversed_pens:
        period_name = "Penalty Shootout"
        timeline_exists = False

        for timeline in timeline_list:
            if timeline.period_name == period_name:
                timeline.shootouts.append(shootout)
                timeline_exists = True
                break

        if not timeline_exists:
            timeline = Timeline(period_name=period_name,
                                goals=[],
                                shootouts=[shootout],
                                cards=[])
            timeline_list.append(timeline)

    reversed_goals = all_cards[::-1]
    for card in reversed_goals:
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
                                shootouts=[],
                                cards=[card])
            timeline_list.append(timeline)

    merged_timeline_list = merge_timeline_objects(timeline_list)

    return merged_timeline_list


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
    date = match.date_utc
    venue = match.match_extra.venue.venue_name if hasattr(match, "match_extra") and hasattr(match.match_extra, "venue") else ""

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
                          time_utc=get_datetime_str(date, time_utc),
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


def get_team_match_details(sport, event):
    team_match = get_field_match_details(sport, event)

    match = event.gender.round.list.match

    update_squads(match, team_match)
    team_match.score_details = update_score(match)
    team_match.timeline = update_timeline(sport, match, team_match.team_a_id, team_match.team_b_id)

    return team_match

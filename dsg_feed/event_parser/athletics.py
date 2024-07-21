import traceback

from models.sport_models.athletics import Contestant, AthleticsEvent, AthleticsTeam, Team


def get_athletics_event_details(sport, event):
    match_round = event.gender.round
    stage = match_round.name
    time_utc = match_round.start_time_utc

    group_name = match_round.name
    event_id = event.discipline_id
    gender = event.gender.value
    event_name = event.name

    high_jump = AthleticsEvent(sport=sport,
                               event=event_name,
                               event_id=event_id,
                               stage=stage,
                               gender=gender,
                               group_name=group_name,
                               time_utc=time_utc,
                               contestant=[])

    return high_jump


def get_athletics_team_event_details(sport, event):
    match_round = event.gender.round
    stage = match_round.name
    time_utc = match_round.time_utc

    group_name = match_round.list.name
    event_id = event.discipline_id
    gender = event.gender.value
    event_name = event.name

    team_obj = AthleticsTeam(sport=sport,
                             event=event_name,
                             event_id=event_id,
                             stage=stage,
                             gender=gender,
                             group_name=group_name,
                             time_utc=time_utc,
                             teams=[])

    return team_obj


def get_athletics_contestant_details(contestant):
    name = contestant.common_name
    athlete_id = contestant.people_id

    country = contestant.nationality_area_name
    country_id = contestant.nationality_area_id
    country_code = contestant.nationality_area_code

    length = None
    time = None
    if hasattr(contestant, "length"):
        length = contestant.length
    if hasattr(contestant, "time"):
        time = contestant.time

    position = contestant.position
    record = contestant.record

    contestant_obj = Contestant(name=name,
                                athlete_id=athlete_id,
                                country=country,
                                country_id=country_id,
                                country_code=country_code,
                                length=length if length else "",
                                time=time if time else "",
                                position=position,
                                record=record,
                                attempt={})
    return contestant_obj


def get_athletics_team_details(team):
    name = team.team_name
    team_id = team.team_id
    country = team.team_area_name
    country_id = team.team_area_id
    country_code = team.team_area_code

    time = team.time
    lane = team.lane
    position = team.position
    record = team.record

    team_obj = Team(name=name,
                    team_id=team_id,
                    country=country,
                    country_id=country_id,
                    country_code=country_code,
                    lane=lane,
                    position=position,
                    record=record,
                    time_utc=time,
                    attempt={},
                    contestants=[])

    for contestant in team.contestants.contestant:
        name = contestant.common_name
        people_id = contestant.people_id
        contestant_obj = Contestant(name=name,
                                    athlete_id=people_id)

        team_obj.contestants.append(contestant_obj)

    return team_obj


# Javelin - can return empty attempts as well
# TODO: check what is length and wind here - in triple jump
# DOCME:

def get_field_event_details(sport, event):
    try:
        event_details = get_athletics_event_details(sport, event)
        contestants_list = event.gender.round.list.contestants

        for contestant in contestants_list.contestant:
            contestant_obj = get_athletics_contestant_details(contestant)
            attempt_keys = [key for key in dir(contestant) if key.startswith("attempt_")]

            for key in attempt_keys:
                attempt = getattr(contestant, key)
                if attempt != '':
                    contestant_obj.attempt[key] = attempt

            event_details.contestant.append(contestant_obj)
        return event_details.to_json()

    except:
        print(traceback.print_exc())


def get_marathon_details(sport, event):
    marathon = get_athletics_event_details(sport, event)
    contestants_list = event.gender.round.list.contestants

    for contestant in contestants_list:
        contestant_obj = get_athletics_contestant_details(contestant)
        attempt_keys = [key for key in dir(contestant) if key.startswith("split_")]

        for key in attempt_keys:
            attempt = contestant.key
            if attempt != '':
                contestant_obj.attempt[key] = attempt

        marathon.contestant.append(contestant_obj)

    return marathon


def get_hurdle_details(sport, event):
    hurdle = get_athletics_event_details(sport, event)
    contestants_list = event.gender.round.list.contestants
    for contestant in contestants_list:
        contestant_obj = get_athletics_contestant_details(contestant)

        contestant_obj.attempt["fail_start"] = contestant.fail_start
        contestant_obj.attempt["lane"] = contestant.lane
        contestant_obj.attempt["reaction_time"] = contestant.reaction_time
        contestant_obj.attempt["yellow_card"] = contestant.yellow_card

        hurdle.contestant.append(contestant_obj)

    return hurdle


def get_relay4x400_details(sport, event):
    relay4x400 = get_athletics_team_event_details(sport, event)
    teams_list = event.gender.round.list.teams.team

    for team in teams_list:
        team_obj = get_athletics_team_details(team)
        attempt_keys = [key for key in dir(team) if key.startswith("split_")]

        for key in attempt_keys:
            attempt = team.key
            if attempt != '':
                team_obj.attempt[key] = attempt

        relay4x400.teams.append(team_obj)

    return relay4x400














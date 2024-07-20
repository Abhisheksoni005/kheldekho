from models.athlete import Athlete
from models.squad import Squad
from utils.data_utils import read_from_json
from models.sport_models.field_sports import TeamEvent

# TODO
# check list.name for badminton
# TODO
# check with support values of match.live - game_minute and period

area_id_map = read_from_json("dataset/country_id_map.json")


def get_single_squads(match, area_id_map):
    contestant_a_id = match.contestant_a_id
    contestant_a_name = match.contestant_a_common_name
    contestant_a_nationality = match.contestant_a_nationality_area_name
    contestant_a_nationality_id = match.contestant_a_nationality_area_id

    contestant_b_id = match.contestant_b_id
    contestant_b_name = match.contestant_b_common_name
    contestant_b_nationality = match.contestant_b_nationality_area_name
    contestant_b_nationality_id = match.contestant_b_nationality_area_id

    if contestant_a_nationality not in area_id_map:
        area_id_map[contestant_a_nationality] = contestant_a_nationality_id
    else:
        if area_id_map[contestant_a_nationality] != contestant_a_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b_nationality not in area_id_map:
        area_id_map[contestant_b_nationality] = contestant_b_nationality_id
    else:
        if area_id_map[contestant_b_nationality] != contestant_b_nationality_id:
            print("Mismatch in nationality id")

    athlete_a = Athlete(id=contestant_a_id, name=contestant_a_name)
    athlete_b = Athlete(id=contestant_b_id, name=contestant_b_name)

    squad_a = Squad(id=contestant_a_nationality_id,
                    name=contestant_a_nationality,
                    size=1,
                    athletes=[athlete_a])

    squad_b = Squad(id=contestant_b_nationality_id,
                    name=contestant_b_nationality,
                    size=1,
                    athletes=[athlete_b])

    return squad_a, squad_b


def get_doubles_squads(match, area_id_map):
    contestant_a1_id = match.contestant_a1_id
    contestant_a1_name = match.contestant_a1_common_name
    contestant_a1_nationality = match.contestant_a1_nationality_area_name
    contestant_a1_nationality_id = match.contestant_a1_nationality_area_id

    contestant_a2_id = match.contestant_a2_id
    contestant_a2_name = match.contestant_a2_common_name
    contestant_a2_nationality = match.contestant_a2_nationality_area_name
    contestant_a2_nationality_id = match.contestant_a2_nationality_area_id

    contestant_b1_id = match.contestant_b1_id
    contestant_b1_name = match.contestant_b1_common_name
    contestant_b1_nationality = match.contestant_b1_nationality_area_name
    contestant_b1_nationality_id = match.contestant_b1_nationality_area_id

    contestant_b2_id = match.contestant_b2_id
    contestant_b2_name = match.contestant_b2_common_name
    contestant_b2_nationality = match.contestant_b2_nationality_area_name
    contestant_b2_nationality_id = match.contestant_b2_nationality_area_id

    if contestant_a1_name == "Ena Shibahara":
        contestant_a1_nationality = 'Japan'
        contestant_a1_nationality_id = '102'

    elif contestant_a2_name == "Ena Shibahara":
        contestant_a2_nationality = 'Japan'
        contestant_a2_nationality_id = '102'

    elif contestant_b1_name == "Ena Shibahara":
        contestant_b1_nationality = 'Japan'
        contestant_b1_nationality_id = '102'

    elif contestant_b2_name == "Ena Shibahara":
        contestant_b2_nationality = 'Japan'
        contestant_b2_nationality_id = '102'

    if contestant_a1_nationality_id != contestant_a2_nationality_id:
        print("Error in Doubles Type Match")

    if contestant_a1_nationality not in area_id_map:
        area_id_map[contestant_a1_nationality] = contestant_a1_nationality_id
    else:
        if area_id_map[contestant_a1_nationality] != contestant_a1_nationality_id:
            print("Mismatch in nationality id")

    if contestant_a2_nationality not in area_id_map:
        area_id_map[contestant_a2_nationality] = contestant_a2_nationality_id
    else:
        if area_id_map[contestant_a2_nationality] != contestant_a2_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b1_nationality_id != contestant_b2_nationality_id:
        print("Error in Doubles Type Match")

    if contestant_b1_nationality not in area_id_map:
        area_id_map[contestant_b1_nationality] = contestant_b1_nationality_id
    else:
        if area_id_map[contestant_b1_nationality] != contestant_b1_nationality_id:
            print("Mismatch in nationality id")

    if contestant_b2_nationality not in area_id_map:
        area_id_map[contestant_b2_nationality] = contestant_b2_nationality_id
    else:
        if area_id_map[contestant_b2_nationality] != contestant_b2_nationality_id:
            print("Mismatch in nationality id")

    athlete_a1 = Athlete(id=contestant_a1_id, name=contestant_a1_name)
    athlete_a2 = Athlete(id=contestant_a2_id, name=contestant_a2_name)
    athlete_b1 = Athlete(id=contestant_b1_id, name=contestant_b1_name)
    athlete_b2 = Athlete(id=contestant_b2_id, name=contestant_b2_name)

    squad_a = Squad(id=contestant_a1_nationality_id,
                    name=contestant_a1_nationality,
                    size=2,
                    athletes=[athlete_a1, athlete_a2])

    squad_b = Squad(id=contestant_b1_nationality_id,
                    name=contestant_b1_nationality,
                    size=2,
                    athletes=[athlete_b1, athlete_b2])

    return squad_a, squad_b


def get_team_squads(match, area_id_map):
    team_a_id = match.team_a_id
    team_a_name = match.team_a_area_name
    team_a_country_id = match.team_a_area_id

    team_b_id = match.team_b_area_id
    team_b_name = match.team_b_area_name
    team_b_country_id = match.team_b_area_id

    if team_a_name not in area_id_map:
        area_id_map[team_a_name] = team_a_country_id
    else:
        if area_id_map[team_a_name] != team_a_country_id:
            print("Mismatch in nationality id")

    if team_b_name not in area_id_map:
        area_id_map[team_b_name] = team_b_country_id
    else:
        if area_id_map[team_b_name] != team_b_country_id:
            print("Mismatch in nationality id")

    squad_a = Squad(id=team_a_country_id,
                    name=team_a_name)

    squad_b = Squad(id=team_b_country_id,
                    name=team_b_name)

    return squad_a, squad_b


def get_lineup_squad(lineup):
    nationalities = set()
    for player in lineup:
        nationalities.add(player.nationality)

    if len(nationalities) != 2:
        print("Error in Lineup")
        raise ValueError("Lineup Error")

    team_a = lineup.filter(lambda x: x.nationality == nationalities[0])
    team_b = lineup.filter(lambda x: x.nationality == nationalities[1])

    squad_a = Squad(id = team_a[0].nationality_area_id,
                    name = team_a[0].nationality,
                    size = len(team_a),
                    athletes = [])

    squad_b = Squad(id = team_b[0].nationality_area_id,
                    name = team_b[0].nationality,
                    size = len(team_b),
                    athletes = [])

    for player in team_a:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position,
                          shirt_number = player.shirtnumber)
        squad_a.athletes.append(athlete)

    for player in team_b:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position,
                          shirt_number = player.shirtnumber)
        squad_b.athletes.append(athlete)


def get_field_match_details(sport, event):
    match_round = event.gender.round
    group_name = match_round.list.name
    stage = match_round.name
    event_id = event.discipline_id
    gender = event.gender.value
    event_name = event.name

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

    teams_obj = TeamEvent(sport=sport,
                          event=event_name,
                          event_id=event_id,
                          gender=gender,
                          match_id=match_id,
                          stage=stage,
                          group_name=group_name,
                          time_utc=time_utc,
                          venue=venue,
                          winner=winner,
                          team_a_id=team_a_id,
                          team_a_name=team_a_area_name,
                          team_a_country=team_a_area_code,
                          team_b_id=team_b_id,
                          team_b_name=team_b_area_name,
                          team_b_country=team_b_area_code,
                          squad_a=[],
                          squad_b=[],
                          coach_a=[],
                          coach_b=[],
                          substitute_a=[],
                          substitute_b=[])

    squad_a, squad_b = get_lineup_squad(match.events.lineups.event)
    coach_a, coach_b = get_lineup_squad(match.events.coaches.event)
    substitute_a, substitute_b = get_lineup_squad(match.events.subs_on_bench.event)
    teams_obj.squad_a = squad_a
    teams_obj.squad_b = squad_b
    teams_obj.coach_a = coach_a
    teams_obj.coach_b = coach_b
    teams_obj.substitute_a = substitute_a
    teams_obj.substitute_b = substitute_b

    sets = []
    for set_number, game in enumerate(match.period_scores.period):
        set_num = set_number + 1
        game_score_a = game.score_a
        game_score_b = game.score_b

        sets.append({
            "set_num": set_num,
            "match_score_a": game_score_a,
            "match_score_b": game_score_b,
        })

    score_a = match.score_a
    score_b = match.score_b
    status = match.status
    winner = match.winner

    if hasattr(match, "contestant_a1_common_name"):
        squad_a, squad_b = get_doubles_squads(match, area_id_map)
        teams_obj.squad_a = squad_a
        teams_obj.squad_b = squad_b

    # Valid for badminton, tennis, beach volleyball
    elif hasattr(match, "contestant_a_common_name"):
        squad_a, squad_b = get_single_squads(match, area_id_map)
        teams_obj.squad_a = squad_a
        teams_obj.squad_b = squad_b

    # Valid for team events
    elif hasattr(match, "events"):
        squad_a, squad_b = get_lineup_squad(match.events.lineups.event)
        coach_a, coach_b = get_lineup_squad(match.events.coaches.event)
        substitute_a, substitute_b = get_lineup_squad(match.events.subs_on_bench.event)

    sets = []
    for set_number, game in enumerate(match.period_scores.period):
        set_num = set_number + 1
        game_score_a = game.score_a
        game_score_b = game.score_b

        sets.append({
            "set_num": set_num,
            "match_score_a": game_score_a,
            "match_score_b": game_score_b,
        })

    score_a = match.score_a
    score_b = match.score_b
    status = match.status
    winner = match.winner


def get_hockey_details(sport, event):
    hockey = get_field_match_details(sport, event)
    return hockey

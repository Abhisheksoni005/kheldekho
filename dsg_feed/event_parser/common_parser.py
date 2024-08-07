from pydantic import BaseModel
from models.squad import Squad
from models.athlete import Athlete
from utils.data_utils import read_from_json

area_id_map = read_from_json("dataset/country_id_map.json")


def get_country_code(winner_nationality_id):
    if not winner_nationality_id:
        return "XXX"
    if winner_nationality_id in area_id_map:
        return area_id_map[winner_nationality_id]["code"]
    return None


class SetScore(BaseModel):
    set_num: int = "0"
    match_score_a: str = "0"
    match_score_b: str = "0"

    def to_json(self):
        return {
            "set_num": self.set_num,
            "match_score_a": self.match_score_a,
            "match_score_b": self.match_score_b
        }


def update_squads(match, event_obj):
    if hasattr(match, "contestant_a1_common_name"):
        squad_a, squad_b = get_doubles_squads(match)
        event_obj.squad_a = squad_a
        event_obj.squad_b = squad_b

    # Valid for badminton, tennis, beach volleyball
    elif hasattr(match, "contestant_a_common_name"):
        squad_a, squad_b = get_single_squads(match)
        event_obj.squad_a = squad_a
        event_obj.squad_b = squad_b

    # Valid for team events - hockey, football, volleyball
    elif hasattr(match, "events"):
        squad_a, squad_b, coach_a, coach_b, substitute_a, substitute_b = None, None, None, None, None, None

        if hasattr(match.events, "lineups") and hasattr(match.events.lineups, "event"):
            squad_a, squad_b = get_lineup_squad(match.events.lineups.event, match.team_a_id, match.team_b_id)
        if hasattr(match.events, "coaches") and hasattr(match.events.coaches, "event"):
            coach_a, coach_b = get_lineup_squad(match.events.coaches.event, match.team_a_id, match.team_b_id)
        if hasattr(match.events, "subs_on_bench") and hasattr(match.events.subs_on_bench, "event"):
            substitute_a, substitute_b = get_lineup_squad(match.events.subs_on_bench.event, match.team_a_id, match.team_b_id)

        event_obj.squad_a = squad_a
        event_obj.squad_b = squad_b
        event_obj.coach_a = coach_a
        event_obj.coach_b = coach_b
        event_obj.substitute_a = substitute_a
        event_obj.substitute_b = substitute_b


def update_team_details(match, event_obj):
    if hasattr(match, "contestant_a1_common_name"):
        event_obj.team_a_id = match.contestant_a1_nationality_area_id
        event_obj.team_a_name = match.contestant_a1_nationality_area_name
        event_obj.team_a_country = match.contestant_a1_nationality_area_code
        event_obj.team_b_id = match.contestant_b1_nationality_area_id
        event_obj.team_b_name = match.contestant_b1_nationality_area_name
        event_obj.team_b_country = match.contestant_b1_nationality_area_code

    elif hasattr(match, "contestant_a_common_name"):
        event_obj.team_a_id = match.contestant_a_nationality_area_id
        event_obj.team_a_name = match.contestant_a_nationality_area_name
        event_obj.team_a_country = match.contestant_a_nationality_area_code
        event_obj.team_b_id = match.contestant_b_nationality_area_id
        event_obj.team_b_name = match.contestant_b_nationality_area_name
        event_obj.team_b_country = match.contestant_b_nationality_area_code
    

def get_single_squads(match):
    contestant_a_id = match.contestant_a_id
    contestant_a_name = match.contestant_a_common_name
    contestant_a_nationality = match.contestant_a_nationality_area_name
    contestant_a_nationality_id = match.contestant_a_nationality_area_id

    contestant_b_id = match.contestant_b_id
    contestant_b_name = match.contestant_b_common_name
    contestant_b_nationality = match.contestant_b_nationality_area_name
    contestant_b_nationality_id = match.contestant_b_nationality_area_id

    if contestant_a_nationality_id not in area_id_map:
        print(contestant_a_nationality_id, contestant_a_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_a_nationality_id != "" and area_id_map[contestant_a_nationality_id]["name"] != contestant_a_nationality:
            print("Mismatch in nationality id")

    if contestant_b_nationality_id not in area_id_map:
        print(contestant_b_nationality_id, contestant_b_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_b_nationality_id != "" and area_id_map[contestant_b_nationality_id]["name"] != contestant_b_nationality:
            print("Mismatch in nationality id")

    athlete_a = Athlete(id=contestant_a_id, name=contestant_a_name)
    athlete_b = Athlete(id=contestant_b_id, name=contestant_b_name)

    squad_a = Squad(id=contestant_a_nationality_id if contestant_a_nationality_id else "",
                    name=contestant_a_nationality if contestant_a_nationality else "TBD",
                    size=1,
                    flag=get_country_code(contestant_a_nationality_id),
                    athletes=[athlete_a])

    squad_b = Squad(id=contestant_b_nationality_id if contestant_b_nationality_id else "",
                    name=contestant_b_nationality if contestant_b_nationality else "TBD",
                    size=1,
                    flag=get_country_code(contestant_b_nationality_id),
                    athletes=[athlete_b])

    return squad_a, squad_b


def get_doubles_squads(match):
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

    if contestant_a1_nationality_id not in area_id_map:
        print(contestant_a1_nationality_id, contestant_a1_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_a1_nationality_id != "" and area_id_map[contestant_a1_nationality_id]["name"] != contestant_a1_nationality:
            print("Mismatch in nationality id")

    if contestant_a2_nationality_id not in area_id_map:
        print(contestant_a2_nationality_id, contestant_a2_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_a2_nationality_id != "" and area_id_map[contestant_a2_nationality_id]["name"] != contestant_a2_nationality:
            print("Mismatch in nationality id")

    if contestant_b1_nationality_id != contestant_b2_nationality_id:
        print("Error in Doubles Type Match")

    if contestant_b1_nationality_id not in area_id_map:
        print(contestant_b1_nationality_id, contestant_b1_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_b1_nationality_id != "" and area_id_map[contestant_b1_nationality_id]["name"] != contestant_b1_nationality:
            print("Mismatch in nationality id")

    if contestant_b2_nationality_id not in area_id_map:
        print(contestant_b2_nationality_id, contestant_b2_nationality)
        raise Exception("New nationality found")
    else:
        if contestant_b2_nationality_id != "" and area_id_map[contestant_b2_nationality_id]["name"] != contestant_b2_nationality:
            print("Mismatch in nationality id")

    athlete_a1 = Athlete(id=contestant_a1_id if contestant_a1_id else "",
                         name=contestant_a1_name if contestant_a1_name else "")
    athlete_a2 = Athlete(id=contestant_a2_id if contestant_a2_id else "",
                         name=contestant_a2_name if contestant_a2_name else "")
    athlete_b1 = Athlete(id=contestant_b1_id if contestant_b1_id else "",
                         name=contestant_b1_name if contestant_b1_name else "")
    athlete_b2 = Athlete(id=contestant_b2_id if contestant_b2_id else "",
                         name=contestant_b2_name if contestant_b2_name else "")

    squad_a = Squad(id=contestant_a1_nationality_id if contestant_a1_nationality_id else "",
                    name=contestant_a1_nationality if contestant_a1_nationality else "TBD",
                    size=2,
                    flag=get_country_code(contestant_a1_nationality_id),
                    athletes=[athlete_a1, athlete_a2])

    squad_b = Squad(id=contestant_b1_nationality_id if contestant_b1_nationality_id else "",
                    name=contestant_b1_nationality if contestant_b1_nationality else "TBD",
                    size=2,
                    flag=get_country_code(contestant_b1_nationality_id),
                    athletes=[athlete_b1, athlete_b2])

    return squad_a, squad_b


def get_team_squads(match):
    team_a_id = match.team_a_id
    team_a_name = match.team_a_area_name
    team_a_country_id = match.team_a_area_id
    team_a_country_code = get_country_code(match.team_a_area_id)

    team_b_id = match.team_b_id
    team_b_name = match.team_b_area_name
    team_b_country_id = match.team_b_area_id
    team_b_country_code = get_country_code(match.team_b_area_id)

    if team_a_name not in area_id_map:
        area_id_map[team_a_name] = team_a_country_id
    else:
        if team_a_name != "" and area_id_map[team_a_name] != team_a_country_id:
            print("Mismatch in nationality id")

    if team_b_name not in area_id_map:
        area_id_map[team_b_name] = team_b_country_id
    else:
        if team_b_name != "" and area_id_map[team_b_name] != team_b_country_id:
            print("Mismatch in nationality id")

    squad_a = Squad(id=team_a_id if team_a_id else "",
                    name=team_a_name if team_a_name else "TBD",
                    flag=team_a_country_code if team_a_country_code else "")

    squad_b = Squad(id=team_b_id if team_b_id else "",
                    name=team_b_name if team_b_name else "TBD",
                    flag=team_b_country_code if team_b_country_code else "")

    return squad_a, squad_b


def get_lineup_squad(lineup, team_a_id, team_b_id):
    nationalities = set()
    for player in lineup:
        nationalities.add(player.team_id)

    if len(nationalities) != 2:
        print("Error in Lineup")
        raise ValueError("Lineup Error")

    team_a = [x for x in lineup if x.team_id == team_a_id]
    team_b = [x for x in lineup if x.team_id == team_b_id]

    squad_a = Squad(id = team_a[0].team_id,
                    name = team_a[0].team_name,
                    size = len(team_a),
                    athletes = [])

    squad_b = Squad(id = team_b[0].team_id,
                    name = team_b[0].team_name,
                    size = len(team_b),
                    athletes = [])

    for player in team_a:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position if hasattr(player, "position") else "",
                          shirt_number = player.shirtnumber if hasattr(player, "shirtnumber") else "")
        squad_a.athletes.append(athlete)

    for player in team_b:
        athlete = Athlete(id = player.people_id,
                          name = player.common_name,
                          position = player.position if hasattr(player, "position") else "",
                          shirt_number = player.shirtnumber if hasattr(player, "shirtnumber") else "")
        squad_b.athletes.append(athlete)

    return squad_a, squad_b


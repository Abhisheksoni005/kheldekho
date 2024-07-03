from models.sport import Sport
from models.event import Event
from models.squad import Squad
from models.match_multi import MatchMulti
from models.match_single import MatchSingle
from utils.data_utils import read_from_json, get_datetime_parsed


def process_match(path):

    response = []
    match_schedule = read_from_json(path)

    for date in match_schedule:
        for event in match_schedule[date]:
            sport_name = event["Sport"]
            sport = Sport(name=sport_name)

            event_name = event["Event"]
            event_obj = Event(parent_sport=sport, name=event_name)

            team_a = None
            team_b = None
            if "Team A" in event and "Team B" in event:
                team_a = event["Team A"]
                team_b = event["Team B"]

            time = event["Time"]
            venue = event["Venue"]
            squad_a = Squad(name=team_a if team_a else "")
            squad_b = Squad(name=team_b if team_b else "")

            try:
                if team_a:
                    match_single = MatchSingle(sport=sport,
                                               event=event_obj,
                                               timestamp=get_datetime_parsed(date, time),
                                               is_live=False,
                                               notification=False,
                                               match_done=False,
                                               team_a=squad_a,
                                               team_b=squad_b,
                                               venue=venue)
                    response.append(match_single)

                else:
                    match_multi = MatchMulti(sport=sport,
                                             event=event_obj,
                                             timestamp=get_datetime_parsed(date, time),
                                             is_live=False,
                                             notification=False,
                                             match_done=False,
                                             venue=venue)
                    response.append(match_multi)
            except Exception as e:
                print(f"Error processing event: {e}")
                raise e

    return response


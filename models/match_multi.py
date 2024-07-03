from dataclasses import field
from datetime import datetime
from typing import List, Dict

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.country import Country
from models.match import Match, Stage
from models.athlete import Athlete, Gender


class MatchMulti(Match):
    sport: Sport = None
    event: Event = None
    timestamp: datetime = None
    is_live: bool = False
    stage: Stage = None
    notification: bool = False
    match_done: bool = False
    venue: str = ""
    number_of_squads: int = 0
    squads: List[Squad] = []
    ranking: Dict[str, int] = dict()

    def display_logic(self):
        return self


# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    event = Event(parent_sport=sport, name="Olympic Basketball Final")

    example_flag = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    country = Country(name="USA", flag=example_flag, gold_medals=30, silver_medals=25, bronze_medals=20)

    athlete1 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender=Gender.MALE, country=country,
                       sports=[sport])
    athlete2 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender=Gender.FEMALE, country=country,
                       sports=[sport])

    athlete3 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender=Gender.MALE, country=country,
                       sports=[sport])
    athlete4 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender=Gender.FEMALE, country=country,
                       sports=[sport])

    squad_a = Squad(name="Team A", size=2, athletes=[athlete1, athlete2])
    squad_b = Squad(name="Team B", size=2, athletes=[athlete3, athlete4])

    match_multi = MatchMulti(
        sport=sport,
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True,
        number_of_squads=2,
        squads=[squad_a, squad_b],
        ranking={squad_a.name: 1, squad_b.name: 2}
    )
    print(match_multi)

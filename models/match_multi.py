from datetime import datetime
from typing import List, Dict, Any

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.match import Match
from models.country import Country
from models.athlete import Athlete, Gender


class MatchMulti(Match):
    id: str = None
    type: str = "2"
    sport: str = None
    event: str = None
    gender: str = ""
    event_id: str = None
    timestamp: datetime = None
    is_live: bool = False
    stage: str = None
    notification: bool = False
    match_done: bool = False
    venue: str = ""
    result_url: str = ""
    status: str = ""
    medal_round: str = "no"
    number_of_squads: int = 0
    squads: List[Squad] = []
    ranking: Dict[str, Any] = dict()

    def display_logic(self):
        return self

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "sport": self.sport,
            "event": self.event,
            "gender": self.gender,
            "event_id": self.event_id,
            "timestamp": str(self.timestamp),
            "is_live": self.is_live,
            "stage": self.stage,
            "notification": self.notification,
            "match_done": self.match_done,
            "venue": self.venue,
            "result_url": self.result_url,
            "status": self.status,
            "medal_round": self.medal_round,
            "number_of_squads": self.number_of_squads,
            "squads": [squad.to_json() for squad in self.squads],
            "ranking": self.ranking
        }

    def __str__(self):
        return f"MatchMulti({self.to_json()})"


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

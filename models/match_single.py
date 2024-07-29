from datetime import datetime
from pydantic import BaseModel

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.match import Match
from models.country import Country
from models.athlete import Athlete, Gender


class Score(BaseModel):
    score_a: int = None
    score_b: int = None

    def to_json(self):
        return {
            "score_a": self.score_a,
            "score_b": self.score_b
        }

    @staticmethod
    def default_score():
        return Score(score_a = 0,
                     score_b = 0)


class MatchSingle(Match):
    id: str = None
    type: str = "1"
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
    medal_round: str = "no"
    team_a: Squad = None
    team_b: Squad = None
    winner: str = None
    status: str = ""
    score: Score = Score.default_score()


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
            "team_a": self.team_a.to_json() if self.team_a else None,
            "team_b": self.team_b.to_json() if self.team_b else None,
            "score": self.score.to_json(),
            "winner": self.winner
        }

    def __str__(self):
        return f"MatchSingle({self.to_json()})"

    def display_logic(self):
        if self.notification and self.timestamp == datetime.fromtimestamp(15000):
            print("Match Started")
            print(f"Score: {self.score.score_a} : {self.score.score_b}")

        if self.notification and self.timestamp == datetime.fromtimestamp(15020):
            print("Match Running")
            print(f"Score: {self.score.score_a} : {self.score.score_b}")


# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    event = Event(parent_sport=sport, name="Olympic Basketball Final")

    example_flag = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    country = Country(name="USA", flag=example_flag, gold_medals=30, silver_medals=25, bronze_medals=20)

    athlete1 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender=Gender.MALE, country=country.name,
                       sport=sport)
    athlete2 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender=Gender.FEMALE, country=country.name,
                       sport=sport)

    athlete3 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender=Gender.MALE, country=country.name,
                       sport=sport)
    athlete4 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender=Gender.FEMALE, country=country.name,
                       sport=sport)

    squad_a = Squad(name="Team A", size=2, athletes=[athlete1, athlete2])
    squad_b = Squad(name="Team B", size=2, athletes=[athlete3, athlete4])
    score = Score(score_a=0, score_b=0)

    match_single = MatchSingle(
        sport=sport.name,
        event=event.name,
        timestamp=datetime.now(),
        is_live=True,
        stage="FINAL",
        notification=True,
        team_a=squad_a,
        team_b=squad_b,
        score=score
    )
    print(match_single)
    match_single.display_logic()

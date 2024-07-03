from datetime import datetime
from dataclasses import field
from pydantic import BaseModel

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.country import Country
from models.match import Match, Stage
from models.athlete import Athlete, Gender


class Score(BaseModel):
    score_a: int
    score_b: int

    @staticmethod
    def default_score():
        return Score(score_a = 0,
                     score_b = 0)


class MatchSingle(Match):
    sport: Sport = None
    event: Event = None
    timestamp: datetime = None
    is_live: bool = False
    stage: Stage = None
    notification: bool = False
    match_done: bool = False
    venue: str = ""
    type: str = "type-1"
    team_a: Squad = None
    team_b: Squad = None
    score: Score = Score.default_score()

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
    score = Score(score_a=0, score_b=0)

    match_single = MatchSingle(
        sport=sport,
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True,
        team_a=squad_a,
        team_b=squad_b,
        score=score
    )
    print(match_single)
    match_single.display_logic()

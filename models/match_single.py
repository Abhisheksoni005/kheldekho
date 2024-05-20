from datetime import datetime
from dataclasses import dataclass, field

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.match import Match, Stage


@dataclass
class Score:
    score_a: int
    score_b: int

    @staticmethod
    def default_score():
        return Score(0, 0)

@dataclass
class MatchSingle(Match):
    team_a: Squad = None
    team_b: Squad = None
    score: Score = field(default_factory=Score.default_score)

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
    squad_a = Squad(name="Team A", members=["Player 1", "Player 2"])
    squad_b = Squad(name="Team B", members=["Player 3", "Player 4"])
    score = Score(score_a=0, score_b=0)

    match_single = MatchSingle(
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True,
        team_a=squad_a,
        team_b=squad_b,
        score=score
    )
    match_single.display_logic()

from typing import List
from datetime import datetime
from pydantic import BaseModel
from models.squad import Squad
from dsg_feed.event_parser.common_parser import SetScore


class ScoreDetails(BaseModel):
    score_a: str = 0
    score_b: str = 0
    sets: List[SetScore] = None

    def to_json(self):
        return {
            "score_a": self.score_a,
            "score_b": self.score_b,
            "sets": [set_score.to_json() for set_score in self.sets] if self.sets else None
        }


class RacquetEvent(BaseModel):
    sport: str = None
    event: str = None
    event_id: str = None
    gender: str = None
    stage: str = None
    season_id: str = None

    match_id: str = None
    group_name: str = None
    time_utc: datetime = None

    winner: str = None
    status: str = None

    squad_a: Squad = None
    squad_b: Squad = None

    team_a_id: str = None
    team_a_name: str = None
    team_a_country: str = None
    team_b_id: str = None
    team_b_name: str = None
    team_b_country: str = None

    score_details: ScoreDetails = None

    def to_json(self):
        return {
            "sport": self.sport,
            "event": self.event,
            "event_id": self.event,
            "gender": self.gender,
            "stage": self.stage,
            "season_id": self.season_id,

            "match_id": self.match_id,
            "group_name": self.group_name,
            "time_utc": str(self.time_utc),

            "winner": self.winner,
            "status": self.status,

            "team_a_id": self.team_a_id,
            "team_a_name": self.team_a_name,
            "team_a_country": self.team_a_country,
            "team_b_id": self.team_b_id,
            "team_b_name": self.team_b_name,
            "team_b_country": self.team_b_country,

            "squad_a": self.squad_a.to_json(),
            "squad_b": self.squad_b.to_json(),
            "score_details": self.score_details.to_json() if self.score_details else None
        }
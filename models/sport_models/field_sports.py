from pydantic import BaseModel
from models.squad import Squad


class TeamEvent(BaseModel):
    sport: str = None
    event: str = None
    event_id: str = None
    gender: str = None

    match_id: str = None
    stage: str = None
    group_name: str = None
    time_utc: str = None
    venue: str = None

    team_a_id: str = None
    team_a_name: str = None
    team_a_country: str = None

    team_b_id: str = None
    team_b_name: str = None
    team_b_country: str = None

    squad_a: Squad = None
    squad_b: Squad = None
    coach_a: Squad = None
    coach_b: Squad = None
    substitute_a: Squad = None
    substitute_b: Squad = None

    score_a: int = 0
    score_b: int = 0
    status: str = None
    winner: str = None

    def to_json_full(self):
        return {
            "sport": self.sport,
            "event": self.event,
            "event_id": self.event,
            "gender": self.gender,
            "match_id": self.match_id,
            "stage": self.stage,
            "group_name": self.group_name,
            "time_utc": self.time_utc,
            "venue": self.venue,
            "team_a_id": self.team_a_id,
            "team_a_name": self.team_a_name,
            "team_a_country": self.team_a_country,
            "team_b_id": self.team_b_id,
            "team_b_name": self.team_b_name,
            "team_b_country": self.team_b_country,
            "squad_a": self.squad_a.to_json() if self.squad_a else None,
            "squad_b": self.squad_b.to_json() if self.squad_b else None,
            "coach_a": self.coach_a.to_json() if self.coach_a else None,
            "coach_b": self.coach_b.to_json() if self.coach_b else None,
            "substitute_a": self.substitute_a.to_json() if self.substitute_a else None,
            "substitute_b": self.substitute_b.to_json() if self.substitute_b else None,
            "score_a": self.score_a,
            "score_b": self.score_b,
            "status": self.status,
            "winner": self.winner
        }

    # remove null keys from json
    def to_json(self):
        return {k: v for k, v in self.to_json().items() if v is not None}












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











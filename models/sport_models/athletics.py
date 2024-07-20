from typing import List
from pydantic import BaseModel


class Contestant(BaseModel):
    name: str = None
    athlete_id: str = None
    country: str = None
    country_id: str = None
    country_code: str = None
    length: str = None
    time: str = None
    position: str = None
    record: str = None
    attempt: dict = None


class AthleticsEvent(BaseModel):
    sport: str = "athletics"
    event: str = None
    event_id: str = None
    stage: str = None
    gender: str = None
    group_name: str = None
    time_utc: str = None
    contestant: List[Contestant] = None


class Team(BaseModel):
    name: str = None
    team_id: str = None
    country: str = None
    country_id: str = None
    country_code: str = None
    lane: str = None
    position: str = None
    record: str = None
    time_utc: str = None
    attempt: dict = None
    contestants: List[Contestant] = None


class AthleticsTeam(BaseModel):
    sport: str = "athletics"
    event: str = None
    event_id: str = None
    stage: str
    gender: str = None
    group_name: str = None
    time_utc: str = None
    teams: List[Team] = None





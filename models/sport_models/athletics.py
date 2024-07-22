from datetime import datetime
from typing import List
from pydantic import BaseModel


class Contestant(BaseModel):
    name: str = None
    athlete_id: str = None
    notification: bool = False
    country: str = None
    country_id: str = None
    country_code: str = None
    length: str = None
    time: str = None
    position: str = None
    record: str = None
    attempt_list: list = None
    attempt_metadata: dict = None

    def to_json(self):
        return {
            "name": self.name,
            "athlete_id": self.athlete_id,
            "notification": self.notification,
            "country": self.country,
            "country_id": self.country_id,
            "country_code": self.country_code,
            "length": self.length,
            "time": self.time,
            "position": self.position,
            "record": self.record,
            "attempt_list": self.attempt_list if self.attempt_list else None,
            "attempt_metadata": self.attempt_metadata if self.attempt_metadata else None
        }


class AthleticsEvent(BaseModel):
    sport: str = "athletics"
    event: str = None
    event_id: str = None
    notification: bool = False
    stage: str = None
    gender: str = None
    group_name: str = None
    time_utc: datetime = None
    status: str = None
    season_id: str = None
    contestant: List[Contestant] = None

    def to_json(self):
        return {
            "sport": self.sport,
            "event": self.event,
            "event_id": self.event_id,
            "notification": self.notification,
            "stage": self.stage,
            "gender": self.gender,
            "group_name": self.group_name,
            "time_utc": str(self.time_utc),
            "status": self.status,
            "season_id": self.season_id,
            "contestant": [contestant.to_json() for contestant in self.contestant]
        }


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

    def to_json(self):
        return {
            "name": self.name,
            "team_id": self.team_id,
            "country": self.country,
            "country_id": self.country_id,
            "country_code": self.country_code,
            "lane": self.lane,
            "position": self.position,
            "record": self.record,
            "time_utc": self.time_utc,
            "attempt": self.attempt,
            "contestants": [contestant.to_json() for contestant in self.contestants]
        }


class AthleticsTeamEvent(BaseModel):
    sport: str = "athletics"
    event: str = None
    event_id: str = None
    notification: bool = False
    stage: str
    gender: str = None
    group_name: str = None
    time_utc: datetime = None
    status: str = None
    season_id: str = None
    teams: List[Team] = None

    def to_json(self):
        return {
            "sport": self.sport,
            "event": self.event,
            "event_id": self.event_id,
            "notification": self.notification,
            "stage": self.stage,
            "gender": self.gender,
            "group_name": self.group_name,
            "time_utc": str(self.time_utc),
            "status": self.status,
            "season_id": self.season_id,
            "teams": [team.to_json() for team in self.teams]
        }






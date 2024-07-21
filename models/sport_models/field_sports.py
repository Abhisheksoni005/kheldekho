from datetime import datetime
from typing import List
from pydantic import BaseModel

from dsg_feed.event_parser.common_parser import SetScore
from models.squad import Squad


class Goals(BaseModel):
    goal_type: str = None
    time: str = None
    extra_time: str = None
    athlete_name: str = None
    athlete_id: str = None
    score_a: str = None
    score_b: str = None
    period: int = None
    team: str = None

    def to_json(self):
        return {
            "goal_type": self.goal_type,
            "time": self.time,
            "extra_time": self.extra_time,
            "athlete_name": self.athlete_name,
            "athlete_id": self.athlete_id,
            "score_a": self.score_a,
            "score_b": self.score_b,
            "period": self.period,
            "team": self.team
        }


class Cards(BaseModel):
    card_type: str = None
    time: str = None
    extra_time: str = None

    athlete_name: str = None
    athlete_id: str = None
    country: str = None
    country_id: str = None
    period: int = None
    team: str = None

    def to_json(self):
        return {
            "card_type": self.card_type,
            "time": self.time,
            "extra_time": self.extra_time,
            "athlete_name": self.athlete_name,
            "athlete_id": self.athlete_id,
            "country": self.country,
            "country_id": self.country,
            "period": self.period,
            "team": self.team
        }


class Timeline(BaseModel):
    period_name: str = None
    goals: List[Goals]
    cards: List[Cards]

    def to_json(self):
        return {
            "period_name": self.period_name,
            "goals": [goal.to_json() for goal in self.goals] if self.goals else None,
            "cards": [card.to_json() for card in self.cards] if self.cards else None
        }


class ScoreDetails(BaseModel):
    score_a: str = 0
    score_b: str = 0
    game_time: str = None
    sets: List[SetScore] = None

    def to_json(self):
        return {
            "score_a": self.score_a,
            "score_b": self.score_b,
            "game_time": self.game_time,
            "sets": [set_score.to_json() for set_score in self.sets] if self.sets else None
        }


class TeamEvent(BaseModel):
    sport: str = None
    event: str = None
    event_id: str = None
    gender: str = None
    stage: str = None

    match_id: str = None
    group_name: str = None
    time_utc: datetime = None
    venue: str = None
    winner: str = None
    status: str = None

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

    score_details: ScoreDetails = None
    timeline: List[Timeline] = None

    def to_json(self):
        return {
            "sport": self.sport,
            "event": self.event,
            "event_id": self.event,
            "gender": self.gender,
            "stage": self.stage,
            "match_id": self.match_id,

            "group_name": self.group_name,
            "time_utc": str(self.time_utc),
            "venue": self.venue,
            "winner": self.winner,
            "status": self.status,

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

            "score_details": self.score_details.to_json() if self.score_details else None,
            "timeline": [timeline.to_json() for timeline in self.timeline] if self.timeline else None
        }













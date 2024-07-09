import json
from typing import Union
from fastapi import APIRouter, HTTPException

from models.match_multi import MatchMulti
from models.match_single import MatchSingle
from service.data_parser import process_match

# In-memory data store for simplicity
data_store = {
    "matches": []
}

router = APIRouter()


@router.get("/all_matches")
def get_all_matches():
    match_schedule = process_match("dataset/date_schedule.json")
    return json.dumps(match_schedule)


@router.get("/matches/{date}/")
def get_matches_by_date(date: str):
    match_schedule = process_match("dataset/date_schedule.json", date=date)
    return json.dumps(match_schedule)


@router.get("/matches/{event_name}", response_model=Union[MatchSingle, MatchMulti])
def get_match(event_name: str):
    match = next((m for m in data_store["matches"] if m.event.name == event_name), None)
    if match:
        return match
    raise HTTPException(status_code=404, detail="Match not found")


@router.post("/matches", response_model=Union[MatchSingle, MatchMulti])
def create_match(match: Union[MatchSingle, MatchMulti]):
    data_store["matches"].append(match)
    return match


@router.put("/matches/{event_name}", response_model=Union[MatchSingle, MatchMulti])
def update_match(event_name: str, match: Union[MatchSingle, MatchMulti]):
    existing_match = next((m for m in data_store["matches"] if m.event.name == event_name), None)
    if existing_match:
        existing_match.timestamp = match.timestamp
        existing_match.is_live = match.is_live
        existing_match.stage = match.stage
        existing_match.notification = match.notification
        if isinstance(existing_match, MatchSingle) and isinstance(match, MatchSingle):
            existing_match.team_a = match.team_a
            existing_match.team_b = match.team_b
            existing_match.score = match.score
        elif isinstance(existing_match, MatchMulti) and isinstance(match, MatchMulti):
            existing_match.number_of_squads = match.number_of_squads
            existing_match.squads = match.squads
            existing_match.ranking = match.ranking
        return existing_match
    raise HTTPException(status_code=404, detail="Match not found")

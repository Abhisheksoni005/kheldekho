from fastapi import APIRouter
from starlette.responses import JSONResponse

from dsg_feed.match_parser import get_match_details
from dsg_feed.schedule_parser import get_schedule_matches

router = APIRouter()


@router.get("/match")
def get_matches(date: str = None, sport: str = None, event_id: str = None, olympics_id: str = "1"):
    match_schedule = get_schedule_matches(day=date, sport_name=sport, discipline_id=event_id, olympics_id=olympics_id)
    return JSONResponse(content=match_schedule)


@router.get("/match/detail")
def get_match_results(sport: str, result_url: str):
    return JSONResponse(content=get_match_details(sport, result_url))
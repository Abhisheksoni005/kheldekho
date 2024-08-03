import traceback

from fastapi import APIRouter
from starlette.responses import JSONResponse

from dsg_feed.match_parser import get_match_details, get_knockout_details
from dsg_feed.schedule_parser import get_schedule_matches

router = APIRouter()


@router.get("/match")
def get_matches(date: str = None, sport: str = None, event_id: str = None, player_id: str = None, olympics_id: str = "72", gender: str = None):
    try:
        match_schedule = get_schedule_matches(day=date, sport_name=sport, discipline_id=event_id, olympics_id=olympics_id, player_id=player_id, gender_filter=gender)
    except:
        print(traceback.format_exc())
        match_schedule = []
    return JSONResponse(content=match_schedule)


@router.get("/match/detail")
def get_match_results(sport: str, result_url: str):
    try:
        details = get_match_details(sport, result_url)
    except:
        print(traceback.format_exc())
        details = {}
    return JSONResponse(content=details)


@router.get("/match/knockouts")
def get_knockout_matches(sport: str, event: str, season_id: str, gender: str):
    try:
        details = get_knockout_details(sport, event, season_id, gender)
    except:
        print(traceback.format_exc())
        details = {}
    return JSONResponse(content=details)


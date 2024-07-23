from fastapi import APIRouter
from starlette.responses import JSONResponse
from dsg_feed.sport_parser import get_events_for_sport_list, get_all_events_list

router = APIRouter()


@router.get("/events")
def get_event_by_sport_name(sport_name: str):
    return JSONResponse(content=get_events_for_sport_list(sport_name))

@router.get("/events/all")
def get_all_events():
    return JSONResponse(content=get_all_events_list())

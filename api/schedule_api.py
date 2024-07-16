import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.data_utils import read_from_json
from dsg_feed.schedule_parser import get_schedule_matches

data_store = {
    "sports": []
}

router = APIRouter()


@router.get("/schedule/get")
def get_schedule():
    return JSONResponse(headers={"Content-Type": "application/json",
                                 "Access-Control-Allow-Origin": "*"},
                        content=read_from_json("dataset/schedule.json"))


@router.get("/schedule/{date}/")
def get_schedule_by_date(date: str):
    match_schedule = get_schedule_matches(day=date)
    return JSONResponse(content=json.dumps(match_schedule))
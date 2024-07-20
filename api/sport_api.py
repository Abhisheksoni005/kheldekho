from models.sport import Sport
from starlette.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from dsg_feed.sport_parser import get_all_sports_list


router = APIRouter()


@router.get("/sports", response_model=Sport)
def get_sport():
    sport_list = get_all_sports_list()
    if sport_list:
        return JSONResponse(content=sport_list)
    raise HTTPException(status_code=404, detail="Sport not found")


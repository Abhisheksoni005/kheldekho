from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.data_utils import read_from_json

data_store = {
    "sports": []
}

router = APIRouter()


@router.get("/get")
def get_schedule():
    return JSONResponse(headers={"Content-Type":"application/json",
                             "Access-Control-Allow-Origin":"*"},
                    content=read_from_json("dataset/schedule.json"))

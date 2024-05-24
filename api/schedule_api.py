from fastapi import APIRouter
from utils.data_utils import read_from_json

data_store = {
    "sports": []
}

router = APIRouter()


@router.get("/get", response_model=dict)
def get_schedule():
    return read_from_json("dataset/schedule.json")

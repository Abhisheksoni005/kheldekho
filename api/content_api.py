from fastapi import APIRouter
from utils.data_utils import read_from_json
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/trivia")
def get_trivia(date: str, sport: str):
    trivia = read_from_json("dataset/trivia.json")
    return JSONResponse(content=trivia[date][sport])


@router.get("/news/home")
def get_news(date: str):
    news_response = read_from_json("dataset/news_home.json")
    return JSONResponse(content=news_response[date])


@router.get("/news/sport")
def get_sport_news(date: str, sport: str):
    news_response = read_from_json("dataset/news_sport.json")
    return JSONResponse(content=news_response[date][sport])

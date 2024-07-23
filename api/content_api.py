from fastapi import APIRouter
from utils.data_utils import read_from_json
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/trivia")
def get_trivia(date: str, sport: str):
    trivia = read_from_json("dataset/trivia.json")
    if date in trivia:
        if sport in trivia[date]:
            return JSONResponse(content=trivia[date][sport])
    return JSONResponse(content={})


@router.get("/news/home")
def get_news(date: str):
    news_response = read_from_json("dataset/news_home.json")
    if not date in news_response:
        return JSONResponse(content=[])
    return JSONResponse(content=news_response[date])


@router.get("/news/sport")
def get_sport_news(date: str, sport: str):
    news_response = read_from_json("dataset/news_sport.json")
    if not date in news_response or not sport in news_response[date]:
        return JSONResponse(content=[])
    return JSONResponse(content=news_response[date][sport])

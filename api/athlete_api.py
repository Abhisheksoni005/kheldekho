from fastapi import APIRouter
from utils.data_utils import read_from_json
from starlette.responses import JSONResponse
from dsg_feed.athlete_parser import get_athletes_data
from models.athlete_detail import AthleteDetail, Story, SocialMedia


router = APIRouter()


@router.get("/athlete/all")
def get_all_athletes(olympics_id: str = "72", country_id = "94"):
    return JSONResponse(content=get_athletes_data(olympics_id, country_id))


def get_athlete_detail_path(id):
    return f"dataset/athlete_detail/{id}/story.json"


@router.get("/athlete_detail")
def get_athlete_detail(player_id: str):
    try:
        path = get_athlete_detail_path(player_id)
        try:
            story_json = read_from_json(path)
            story = Story.dict_to_story(story_json)
        except Exception as e:
            story = Story(social_media=SocialMedia())

        athletes_json = read_from_json("dataset/athletes.json")
        athlete = next((a for a in athletes_json if a["id"] == player_id), None)

        response = AthleteDetail(
            id=player_id,
            deeplink_to_share="",
            country=athlete["country"],
            flag=athlete["country_code"],
            sport=athlete["sports"],
            profile_image_url=athlete["profile_image_url"] if athlete["profile_image_url"] in athlete else "",
            story=story,
            news=[]
        )

    except Exception as e:
        response = AthleteDetail(
            id=player_id,
            deeplink_to_share="",
            country="",
            flag="",
            sport="",
            profile_image_url="",
            story=Story(social_media=SocialMedia()),
            news=[]
        )

    return response.to_json()

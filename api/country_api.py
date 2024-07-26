import requests
from fastapi import APIRouter
from requests.auth import HTTPBasicAuth
from models.country import  CountryResponse
from starlette.responses import JSONResponse
from utils.data_utils import read_from_json, dict_to_object

router = APIRouter()

BASE_API_URL = "https://dsg-api.com/clients/"
username = "samarth"
password = "SdW!eH7x6&"
AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"

f_type = "json"


@router.get("/countries")
async def get_all_countries():
    return JSONResponse(content=get_countries())


@router.get("/medals")
async def get_medals_tokyo(olympics_id: int = "72"):
    if olympics_id == "1":
        medal_tally = read_from_json("dataset/medal_tokyo.json")
    else:
        medal_tally = get_paris_tally(olympics_id)
    return JSONResponse(content=medal_tally)


def get_total_medals(gold, silver, bronze):
    total_medal = 0
    if gold:
        total_medal += int(gold)
    if silver:
        total_medal += int(silver)
    if bronze:
        total_medal += int(bronze)
    return total_medal


def get_paris_tally(olympics_id: int = "72"):
    api_path = f"{BASE_API_URL}samarth/multisport/get_medals?id={olympics_id}&client={username}&authkey={AUTH_KEY}"
    api_path += f"&ftype={f_type}"
    result_response = requests.get(api_path,
                                   auth=HTTPBasicAuth(username, password)
                                   )

    result_json = result_response.json()
    result = dict_to_object(result_json)

    tally = result.datasportsgroup.multisport_event.multisport_event_season.medal_table
    if hasattr(tally, "table"):
        medal_tally = []
        india_obj = {}
        for country in tally.table:
            medal_obj = {
                "country_id": country.area_id,
                "country_name": country.country,
                "gold": country.gold,
                "silver": country.silver,
                "bronze": country.bronze,
                "total": get_total_medals(country.gold, country.silver, country.bronze),
                "rank": country.position,
                "flag": country.area_code
            }
            if country.area_code == "IND":
                india_obj = medal_obj
                continue
            medal_tally.append(medal_obj)
        medal_tally.insert(3, india_obj)
        return medal_tally

    response_list = read_from_json("dataset/medal_tokyo.json")
    for country in response_list:
        country["gold"] = 0
        country["silver"] = 0
        country["bronze"] = 0
        country["total"] = 0
        country["rank"] = "-"
    return response_list


def get_countries():

    result_url = f"{BASE_API_URL}samarth/multisport/get_areas?client={username}&authkey={AUTH_KEY}"
    result_url += f"&ftype={f_type}"
    result_response = requests.get(result_url,
                                   auth=HTTPBasicAuth(username, password)
                                   )

    result_json = result_response.json()
    result = dict_to_object(result_json)

    country_dict = {}
    for country in result.datasportsgroup.area:
        country_obj = CountryResponse(id=country.area_id, name=country.name, code=country.country_code)
        country_dict[country.area_id] = country_obj.to_json()

    return country_dict



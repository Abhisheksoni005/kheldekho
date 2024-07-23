import requests
from fastapi import APIRouter
from requests.auth import HTTPBasicAuth
from models.country import  CountryResponse
from starlette.responses import JSONResponse
from utils.data_utils import read_from_json, dict_to_object

router = APIRouter()


@router.get("/countries")
async def get_all_countries():
    return JSONResponse(content=get_countries())


@router.get("/medals")
async def get_medals_tokyo(olympics_id: int = "72"):
    medal_tally = read_from_json("dataset/medal_tokyo.json")
    return JSONResponse(content=medal_tally)


def get_countries():
    BASE_API_URL = "https://dsg-api.com/clients/"
    username = "samarth"
    password = "SdW!eH7x6&"
    AUTH_KEY = "VoT5fdaqbsg6IyCSZPKYn3WUQ9FxzkD4LAh"

    f_type = "json"
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



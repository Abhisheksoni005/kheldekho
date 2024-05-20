from models.country import Country
from fastapi import HTTPException, APIRouter

data_store = {
    "countries": []
}

router = APIRouter()


@router.get("/get/{name}", response_model=Country)
async def get_country(name: str):
    country = next((c for c in data_store["countries"] if c.name == name), None)
    if country:
        return country
    raise HTTPException(status_code=404, detail="Country not found")


@router.post("/create", response_model=Country)
async def create_country(country: Country):
    data_store["countries"].append(country)
    return country


@router.put("/update/{name}", response_model=Country)
async def update_country(name: str, country: Country):
    existing_country = next((c for c in data_store["countries"] if c.name == name), None)
    if existing_country:
        existing_country.flag = country.flag
        existing_country.gold_medals = country.gold_medals
        existing_country.silver_medals = country.silver_medals
        existing_country.bronze_medals = country.bronze_medals
        return existing_country
    raise HTTPException(status_code=404, detail="Country not found")
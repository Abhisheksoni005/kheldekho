from models.sport import Sport
from fastapi import APIRouter, HTTPException


data_store = {
    "sports": []
}

router = APIRouter()


@router.get("/sports/{name}", response_model=Sport)
def get_sport(name: str):
    sport = next((s for s in data_store["sports"] if s.name == name), None)
    if sport:
        return sport
    raise HTTPException(status_code=404, detail="Sport not found")


@router.post("/sports", response_model=Sport)
def create_sport(sport: Sport):
    data_store["sports"].append(sport)
    return sport


@router.put("/sports/{name}", response_model=Sport)
def update_sport(name: str, sport: Sport):
    existing_sport = next((s for s in data_store["sports"] if s.name == name), None)
    if existing_sport:
        existing_sport.icon = sport.icon
        return existing_sport
    raise HTTPException(status_code=404, detail="Sport not found")

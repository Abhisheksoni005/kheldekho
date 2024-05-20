from models.athlete import Athlete
from fastapi import APIRouter, HTTPException


# In-memory data store for simplicity
data_store = {
    "athletes": []
}

router = APIRouter()


@router.get("/get/{name}", response_model=Athlete)
def get_athlete(name: str):
    athlete = next((a for a in data_store["athletes"] if a.name == name), None)
    if athlete:
        return athlete
    raise HTTPException(status_code=404, detail="Athlete not found")


@router.post("/create/athletes", response_model=Athlete)
def create_athlete(athlete: Athlete):
    data_store["athletes"].append(athlete)
    return athlete


@router.put("/update/{name}", response_model=Athlete)
def update_athlete(name: str, athlete: Athlete):
    existing_athlete = next((a for a in data_store["athletes"] if a.name == name), None)
    if existing_athlete:
        existing_athlete.date_of_birth = athlete.date_of_birth
        existing_athlete.gender = athlete.gender
        existing_athlete.country = athlete.country
        existing_athlete.sports = athlete.sports
        return existing_athlete
    raise HTTPException(status_code=404, detail="Athlete not found")

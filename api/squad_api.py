from models.squad import Squad
from fastapi import APIRouter, HTTPException


data_store = {
    "squads": []
}

router = APIRouter()


@router.get("/squads/{name}", response_model=Squad)
def get_squad(name: str):
    squad = next((s for s in data_store["squads"] if s.name == name), None)
    if squad:
        return squad
    raise HTTPException(status_code=404, detail="Squad not found")


@router.post("/squads", response_model=Squad)
def create_squad(squad: Squad):
    data_store["squads"].append(squad)
    return squad


@router.put("/squads/{name}", response_model=Squad)
def update_squad(name: str, squad: Squad):
    existing_squad = next((s for s in data_store["squads"] if s.name == name), None)
    if existing_squad:
        existing_squad.size = squad.size
        existing_squad.athletes = squad.athletes
        return existing_squad
    raise HTTPException(status_code=404, detail="Squad not found")

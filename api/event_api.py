from models.event import Event
from fastapi import HTTPException, APIRouter

data_store = {
    "events": []
}

router = APIRouter()


@router.get("/events/{name}", response_model=Event)
def get_event(name: str):
    event = next((e for e in data_store["events"] if e.name == name), None)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.post("/events", response_model=Event)
def create_event(event: Event):
    data_store["events"].append(event)
    return event


@router.put("/events/{name}", response_model=Event)
def update_event(name: str, event: Event):
    existing_event = next((e for e in data_store["events"] if e.name == name), None)
    if existing_event:
        existing_event.parent_sport = event.parent_sport
        existing_event.name = event.name
        return existing_event
    raise HTTPException(status_code=404, detail="Event not found")
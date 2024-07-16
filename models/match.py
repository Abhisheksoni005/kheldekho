from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from models.event import Event
from models.sport import Sport


class Match(BaseModel):
    id: str = None
    type: str = "0"
    sport: str
    event: str
    event_id: str = None
    timestamp: datetime
    is_live: bool
    stage: str
    notification: bool
    match_done: bool = False
    medal_round: str = "no"
    venue: str = ""
    result_url: str = ""
    gender: str = ""


# Example usage:
if __name__ == "__main__":
    sport = "Basketball"
    event = "Olympic Basketball Final"
    match = Match(
        sport=sport,
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage="FINAL",
        notification=True
    )
    print(match)

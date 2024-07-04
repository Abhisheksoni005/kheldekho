from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from models.event import Event
from models.sport import Sport


class Stage(Enum):
    QUALIFIER = "QUALIFIER"
    GROUP_STAGE = "GROUP_STAGE"
    RO16 = "RO16"
    QUARTER_FINALS = "QUARTER_FINALS"
    SEMI_FINALS = "SEMI_FINALS"
    FINAL = "FINAL"


class Match(BaseModel):
    id: str = None
    type: str = "0"
    sport: str
    event: str
    timestamp: datetime
    is_live: bool
    stage: Stage
    notification: bool
    match_done: bool  = False
    venue: str = ""


# Example usage:
if __name__ == "__main__":
    sport = "Basketball"
    event = "Olympic Basketball Final"
    match = Match(
        sport=sport,
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True
    )
    print(match)

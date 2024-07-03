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
    sport: Sport
    event: Event
    timestamp: datetime
    is_live: bool
    stage: Stage
    notification: bool
    match_done: bool
    venue: str


# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    event = Event(parent_sport=sport, name="Olympic Basketball Final")
    match = Match(
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True
    )
    print(match)

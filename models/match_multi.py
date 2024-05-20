from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

from models.event import Event
from models.sport import Sport
from models.squad import Squad
from models.match import Match, Stage


@dataclass
class MatchMulti(Match):
    number_of_squads: int = 0
    squads: List[Squad] = field(default_factory=list)
    ranking: Dict[Squad, int] = field(default_factory=dict)

    def display_logic(self):
        return self


# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    event = Event(parent_sport=sport, name="Olympic Basketball Final")
    squad1 = Squad(name="Team A", members=["Player 1", "Player 2"])
    squad2 = Squad(name="Team B", members=["Player 3", "Player 4"])

    match_multi = MatchMulti(
        event=event,
        timestamp=datetime.now(),
        is_live=True,
        stage=Stage.FINAL,
        notification=True,
        number_of_squads=2,
        squads=[squad1, squad2],
        ranking={squad1: 1, squad2: 2}
    )
    print(match_multi)

from typing import List
from datetime import datetime
from pydantic import BaseModel

from models.athlete import Athlete, Gender
from models.sport import Sport


class Squad(BaseModel):
    id: str = None
    name: str
    flag: str = None
    size: int = 0
    athletes: List[Athlete] = []

    def to_json(self):
        return {
            "name": self.name,
            "flag": self.flag,
            "size": self.size,
            "athletes": [athlete.to_json() for athlete in self.athletes]
        }

# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    athlete1 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender=Gender.MALE, country="USA", sport=sport)
    athlete2 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender=Gender.FEMALE, country="USA", sport=sport)

    squad = Squad(name="Team A", flag = "", size=2, athletes=[athlete1, athlete2])
    print(squad)

from typing import List
from datetime import datetime
from pydantic import BaseModel

from models.athlete import Athlete


class Squad(BaseModel):
    name: str
    size: int = 0
    athletes: List[Athlete] = []

# Example usage:
if __name__ == "__main__":
    athlete1 = Athlete(name="John Doe", date_of_birth=datetime(1990, 1, 1), gender="Male", country="USA", sports=["Basketball"])
    athlete2 = Athlete(name="Jane Smith", date_of_birth=datetime(1992, 5, 15), gender="Female", country="USA", sports=["Basketball"])

    squad = Squad(name="Team A", size=2, athletes=[athlete1, athlete2])
    print(squad)

from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel

from models.sport import Sport
from models.country import Country


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Athlete(BaseModel):
    name: str
    date_of_birth: datetime
    gender: Gender
    country: Country
    sports: List[Sport]
    events: List[str] = []

# Example usage:
if __name__ == "__main__":
    example_flag = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    country = Country(name="USA", flag=example_flag, gold_medals=30, silver_medals=25, bronze_medals=20)
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    athlete = Athlete(
        name="John Doe",
        date_of_birth=datetime(1990, 1, 1),
        gender=Gender.MALE,
        country=country,
        sports=[sport]
    )
    print(athlete)

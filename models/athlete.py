from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from models.sport import Sport
from models.country import Country


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Athlete(BaseModel):
    id: str = None
    name: str
    date_of_birth: datetime = None
    gender: Gender = None
    country: str = None
    sport: Sport = None
    profile_image_url: str = None
    position: str = None
    shirt_number: str = None

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": str(self.date_of_birth),
            "gender": self.gender,
            "country": self.country,
            "sports": self.sport.to_json() if self.sport else None,
            "profile_image_url": self.profile_image_url,
            "position": self.position,
            "shirt_number": self.shirt_number
        }


# Example usage:
if __name__ == "__main__":
    example_flag = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    country = Country(name="USA", flag=example_flag, gold_medals=30, silver_medals=25, bronze_medals=20)
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    athlete = Athlete(
        id="1",
        name="John Doe",
        date_of_birth=datetime(1990, 1, 1),
        gender=Gender.MALE,
        country=country.name,
        sport=sport,
        profile_image_url="https://example.com/profile.jpg"
    )
    print(athlete)

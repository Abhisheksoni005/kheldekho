from pydantic import BaseModel


class MedalTally(BaseModel):
    name: str
    gold: int
    silver: int
    bronze: int
    total: int
    rank: int
    flag: str

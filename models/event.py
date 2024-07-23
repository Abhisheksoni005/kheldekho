from pydantic import BaseModel
from models.sport import Sport


class Event(BaseModel):
    id: str = None
    name: str = None
    type: str = None
    parent_sport: str = None

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent_sport": self.parent_sport
        }

# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    event = Event(parent_sport=sport.name, name="Olympic Basketball Final")
    print(event)

from pydantic import BaseModel


class Sport(BaseModel):
    id: str = None
    name: str
    type: str = None

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }

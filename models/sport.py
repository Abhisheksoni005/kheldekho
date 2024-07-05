from pydantic import BaseModel


class Sport(BaseModel):
    id: str = None
    name: str
    icon: bytes = None  # Use bytes to represent Blob in Python

    def to_json(self):
        return {
            "name": self.name,
            "icon": self.icon
        }

# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    print(sport)

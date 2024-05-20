from pydantic import BaseModel


class Sport(BaseModel):
    name: str
    icon: bytes

# Example usage:
if __name__ == "__main__":
    example_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    sport = Sport(name="Basketball", icon=example_icon)
    print(sport)

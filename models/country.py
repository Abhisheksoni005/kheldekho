from pydantic import BaseModel


class Country(BaseModel):
    name: str
    flag: bytes  # Use bytes to represent Blob in Python
    gold_medals: int
    silver_medals: int
    bronze_medals: int


class CountryResponse(BaseModel):
    id: str
    name: str
    code: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }


# Example usage
if __name__ == "__main__":
    example_flag = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10...'
    country = Country(name="USA", flag=example_flag, gold_medals=30, silver_medals=25, bronze_medals=20)
    print(country)

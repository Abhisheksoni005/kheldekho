from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    last_logged_in: datetime

# Example usage:
if __name__ == "__main__":
    user = User(
        email="user@example.com",
        username="user123",
        last_logged_in=datetime.now()
    )
    print(user)

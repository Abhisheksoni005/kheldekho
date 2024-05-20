from models.user import User
from fastapi import HTTPException, APIRouter

data_store = {
    "users": []
}

router = APIRouter()


@router.get("/users/{username}", response_model=User)
def get_user(username: str):
    user = next((u for u in data_store["users"] if u.username == username), None)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/users", response_model=User)
def create_user(user: User):
    data_store["users"].append(user)
    return user


@router.put("/users/{username}", response_model=User)
def update_user(username: str, user: User):
    existing_user = next((u for u in data_store["users"] if u.username == username), None)
    if existing_user:
        existing_user.email = user.email
        existing_user.last_logged_in = user.last_logged_in
        return existing_user
    raise HTTPException(status_code=404, detail="User not found")
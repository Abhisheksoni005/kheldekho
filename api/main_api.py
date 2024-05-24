import uvicorn
from fastapi import FastAPI
from user_api import router as user_router
from sport_api import router as sport_router
from event_api import router as event_router
from match_api import router as match_router
from squad_api import router as squad_router
from country_api import router as country_router
from athlete_api import router as athlete_router
from schedule_api import router as schedule_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(sport_router, prefix="/sport")
app.include_router(match_router, prefix="/match")
app.include_router(squad_router, prefix="/squad")
app.include_router(country_router, prefix="/country")
app.include_router(athlete_router, prefix="/athlete")
app.include_router(schedule_router, prefix="/schedule")

allowed_origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Run the app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000,
                )

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.user_api import router as user_router
from api.sport_api import router as sport_router
from api.event_api import router as event_router
from api.match_api import router as match_router
from api.squad_api import router as squad_router
from api.country_api import router as country_router
from api.athlete_api import router as athlete_router
from api.schedule_api import router as schedule_router


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(sport_router, prefix="/sport")
app.include_router(match_router, prefix="/match")
app.include_router(squad_router, prefix="/squad")
app.include_router(country_router, prefix="/country")
app.include_router(athlete_router, prefix="/athlete")
app.include_router(schedule_router, prefix="/schedule")

allowed_origins = ["http://localhost:3000",
                   "https://localhost:3000",
                   "http://kheldekho.in",
                   "http://kheldekho.in:3000",
                   "https://kheldekho.in",
                   "https://kheldekho.in:3000",
                   "http://20.197.9.130"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ssl_certfile = r"/home/ec2-user/cert/kheldekho_in.crt"
ssl_keyfile = r"/home/ec2-user/cert/key_final.key"


if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000,
                ssl_keyfile=ssl_keyfile,
                ssl_certfile=ssl_certfile,
                )

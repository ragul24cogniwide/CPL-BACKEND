from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import players, teams, tournaments, matches
from dotenv import load_dotenv

load_dotenv()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CPL Backend API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(tournaments.router)
app.include_router(matches.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CPL Backend API (FastAPI)"}

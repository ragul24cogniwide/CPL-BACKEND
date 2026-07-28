from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from . import models
from .routers import players, teams, tournaments, matches, auth, users
from .auth_utils import get_password_hash
from dotenv import load_dotenv

load_dotenv()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CPL Backend API", version="1.0.0")

@app.on_event("startup")
def seed_admin_user():
    db: Session = SessionLocal()
    try:
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin_user:
            print("Seeding default admin user...")
            hashed_password = get_password_hash("admin@123")
            new_admin = models.User(
                username="admin",
                hashed_password=hashed_password,
                role="admin"
            )
            db.add(new_admin)
            db.commit()
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(players.router)
app.include_router(teams.router)
app.include_router(tournaments.router)
app.include_router(matches.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CPL Backend API (FastAPI)"}

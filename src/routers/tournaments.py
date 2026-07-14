from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/tournaments", tags=["Tournaments"])

@router.get("", response_model=List[schemas.Tournament])
def get_tournaments(db: Session = Depends(get_db)):
    tournaments = db.query(models.Tournament).options(joinedload(models.Tournament.teams)).all()
    return tournaments

@router.post("", response_model=schemas.Tournament)
def create_tournament(tournament: schemas.TournamentCreate, db: Session = Depends(get_db)):
    tournament_data = tournament.model_dump(exclude={"teamIds"})
    db_tournament = models.Tournament(**tournament_data)
    
    if tournament.teamIds:
        teams = db.query(models.Team).filter(models.Team.id.in_(tournament.teamIds)).all()
        db_tournament.teams = teams
        
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@router.put("/{tournament_id}", response_model=schemas.Tournament)
def update_tournament(tournament_id: str, tournament: schemas.TournamentUpdate, db: Session = Depends(get_db)):
    db_tournament = db.query(models.Tournament).options(joinedload(models.Tournament.teams)).filter(models.Tournament.id == tournament_id).first()
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    update_data = tournament.model_dump(exclude={"teamIds"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tournament, key, value)
        
    if tournament.teamIds is not None:
        teams = db.query(models.Team).filter(models.Team.id.in_(tournament.teamIds)).all()
        db_tournament.teams = teams
        
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: str, db: Session = Depends(get_db)):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    db.delete(db_tournament)
    db.commit()
    return {"message": "Tournament deleted"}

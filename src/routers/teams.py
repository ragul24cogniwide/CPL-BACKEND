from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/teams", tags=["Teams"])

@router.get("", response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).options(joinedload(models.Team.players)).all()
    return teams

@router.post("", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    team_data = team.model_dump(exclude={"playerIds"})
    db_team = models.Team(**team_data)
    
    if team.playerIds:
        players = db.query(models.Player).filter(models.Player.id.in_(team.playerIds)).all()
        db_team.players = players
        
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.put("/{team_id}", response_model=schemas.Team)
def update_team(team_id: str, team: schemas.TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(models.Team).options(joinedload(models.Team.players)).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    update_data = team.model_dump(exclude={"playerIds"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
        
    if team.playerIds is not None:
        players = db.query(models.Player).filter(models.Player.id.in_(team.playerIds)).all()
        db_team.players = players
        
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/{team_id}")
def delete_team(team_id: str, db: Session = Depends(get_db)):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted"}

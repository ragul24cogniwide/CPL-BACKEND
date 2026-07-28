from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth_utils import get_current_admin_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    return db.query(models.User).all()

@router.put("/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(
    user_id: str,
    role_update: schemas.UserRoleUpdate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if role_update.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'user'")
        
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user

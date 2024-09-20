from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from authentication import get_current_active_user
from database import get_db
from repository import user_crud
from schemas import User, UserCreate, UserDisplay

router = APIRouter(
        prefix="/user",
        tags=["Users"]
)


@router.post("/")
def create_user(request: UserCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):
    """Create new user"""
    return user_crud.create(request, db)


@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get user detail based on ID"""
    user = user_crud.get_user(id, db)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found with ID as {id}"
        )
    return user

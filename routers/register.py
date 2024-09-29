from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import user_crud
from schemas import UserCreate, UserDisplay

router = APIRouter(
        prefix="/register",
        tags=["Authentication"]
)


@router.post("/", response_model=UserDisplay)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create(request, db)

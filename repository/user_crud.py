from typing import Type

from sqlalchemy.orm import Session

import models
from authentication import get_password_hash
from schemas import UserCreate


def get_user(id: int, db: Session):
    user: Type[models.User] | None = db.query(models.User).filter(models.User.id == id).first()
    return user if user else None


def create(request: UserCreate, db: Session):
    request.password = get_password_hash(request.password)
    new_user: models.User = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_from_email(email: str, db: Session):
    user: Type[models.User] | None = db.query(models.User).filter(models.User.email == email).first()
    return user if user else None

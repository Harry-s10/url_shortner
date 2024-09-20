import random
import string
from datetime import datetime, timedelta
from typing import Type
from urllib.parse import urlparse

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models


def generate_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_short_url(url: str, db: Session):
    existing_url_record: Type[models.URLS] | None = db.query(models.URLS).filter(models.URLS.long_url == url).first()
    if existing_url_record:
        if existing_url_record.expiry < datetime.utcnow():
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"http://localhost:8000/{existing_url_record.short_url} is expired"
            )
        return existing_url_record
    short_code: str = generate_code()
    while db.query(models.URLS).filter(models.URLS.short_url == short_code).first():
        short_code: str = generate_code()
    new_url: models.URLS = models.URLS(long_url=url, short_url=short_code,
                                       expiry=datetime.utcnow() + timedelta(minutes=2))
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


def get_url_record(short_code: str, db: Session):
    url_record = db.query(models.URLS).filter(models.URLS.short_url == short_code).first()
    return url_record if url_record else None


def absolute_url(url: str):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f"http://{url}"
    return url


def extend_url_expiry(short_code: str, db: Session, extend_time: int = 2):
    url_record = db.query(models.URLS).filter(models.URLS.short_url == short_code).first()
    if not url_record:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No URL found with {short_code} code"
        )
    url_record.expiry = datetime.utcnow() + timedelta(minutes=extend_time)
    db.commit()
    return "Extended"


def log_url_access(db: Session, url_id: int, ip_address: str, user_agent: str):
    access_log: models.URLAccessLogs = models.URLAccessLogs(
            url_id=url_id,
            ip_address=ip_address,
            user_agent=user_agent
    )
    db.add(access_log)
    db.commit()


def get_url_access_logs(db: Session, url_id: int):
    access_logs = db.query(models.URLAccessLogs).filter(models.URLAccessLogs.url_id == url_id).all()
    return access_logs

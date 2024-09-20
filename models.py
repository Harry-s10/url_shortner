from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from database import Base

pwd_content = CryptContext(schemes=['bcrypt'], deprecated="auto")


class URLS(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    long_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=False)
    access_logs = Relationship("URLAccessLogs", back_populates="urls")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_content.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_content.verify(plain_password, hashed_password)


class URLAccessLogs(Base):
    __tablename__ = "url_access_logs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    access_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    urls = Relationship("URLS", back_populates="access_logs")

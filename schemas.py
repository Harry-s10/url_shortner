from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    id: int
    is_active: bool
    model_config = {
        "from_attributes": True
    }


class UserDisplay(UserBase):
    id: int
    is_active: bool
    model_config = {
        "from_attributes": True
    }


class URLBase(BaseModel):
    long_url: str
    model_config = {
        "from_attributes": True
    }


class URLCreate(URLBase):
    short_url: str
    expiry: datetime
    model_config = {
        "from_attributes": True
    }


class URL(URLCreate):
    id: int


class URLAccessLog(BaseModel):
    id: int
    access_time: datetime
    ip_address: str
    user_agent: str
    model_config = {
        "from_attributes": True
    }


class URLAnalytics(URL):
    click_count: int
    logs: List[URLAccessLog]
    model_config = {
        "from_attributes": True
    }
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
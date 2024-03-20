from __future__ import annotations
from pydantic import BaseModel, validator
from typing import List, Optional, Annotated
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel

SECRET_KEY = "d4df28b301f4518d2bdce68cb868e8e19340c4a059a3470232815bc52432d95b"
ALGORITHM = "HS256"
ACCESS_TOCKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None  


from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True

class User(UserInDB):
    id: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class PreferenceBase(BaseModel):
    weather: str
    activity_type: str
    activity: str
    preference_score: float


class RecommendationCreate(BaseModel):
    weather: str
    activity_type: str
    activity: str




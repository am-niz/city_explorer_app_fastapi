from pydantic import BaseModel
from typing import List, Optional
from __future__ import annotations

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    preferences: List[Preference] = []

    class Config:
        orm_mode = True

class PreferenceBase(BaseModel):
    activity_type: str
    preference_score: float

class PreferenceCreate(PreferenceBase):
    pass

class Preference(PreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class RecommendationBase(BaseModel):
    activity: str
    weather_condition: str
    created_at: Optional[str]

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

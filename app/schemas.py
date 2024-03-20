from __future__ import annotations
from pydantic import BaseModel, validator
from typing import List, Optional







class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    email: str

# class User(UserBase):
#     id: int
#     preferences: List[Preference] = []

#     class Config:
#         orm_mode = True

class PreferenceBase(BaseModel):
    weather: str
    activity_type: str
    activity: str
    preference_score: float

# class PreferenceCreate(PreferenceBase):
#     pass

class PreferenceResponse(PreferenceBase):
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True

class RecommendationCreate(BaseModel):
    weather: str
    temperature: float
    humidity: float
    activity_type: str
    activity: str


# class RecommendationCreate(RecommendationBase):
#     pass

# class Recommendation(RecommendationBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True

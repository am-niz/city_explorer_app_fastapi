from __future__ import annotations
from pydantic import BaseModel, validator
from typing import List, Optional



# city_name_pattern = r'^[a-zA-Z\s-]+$'  # Allows letters, spaces, and hyphens



class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# class UserBase(UserCreate):
#     username: str
#     email: str

# class User(UserBase):
#     id: int
#     preferences: List[Preference] = []

#     class Config:
#         orm_mode = True

# class PreferenceBase(BaseModel):
#     activity_type: str
#     preference_score: float

# class PreferenceCreate(PreferenceBase):
#     pass

# class Preference(PreferenceBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True

# class RecommendationBase(BaseModel):
#     activity: str
#     weather_condition: str
#     created_at: Optional[str]

# class RecommendationCreate(RecommendationBase):
#     pass

# class Recommendation(RecommendationBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True

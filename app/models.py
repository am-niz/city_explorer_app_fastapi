from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    preferences = relationship("Preference", back_populates="user")

class Preference(Base): 
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    weather = Column(String, index=True)
    activity_type = Column(String, index=True)
    activity = Column(String, index=True)
    preference_score = Column(Float, index=True)
    user = relationship("User", back_populates="preferences")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    weather = Column(String, index=True)
    activity_type = Column(String, index=True)
    activity = Column(String, index=True)

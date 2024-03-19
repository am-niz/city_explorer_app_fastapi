from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    # preferences = relationship("Preference", back_populates="user")

# class Preference(Base): 
#     __tablename__ = "preferences"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     activity_type = Column(String, index=True)
#     Preference_score = Column(Float)
#     user = relationship("User", back_populates="preferences")

# class Recommendation(Base):
#     __tablename__ = "recommendations"

#     id = Column(Integer, unique=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     activity = Column(String)
#     weather_condition = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     user = relationship("User", back_populates="recommendations")

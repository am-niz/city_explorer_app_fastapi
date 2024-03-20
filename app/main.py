from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from models import Preference
import re
from schemas import UserCreate, UserBase, PreferenceBase, PreferenceResponse
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def validate_email(email: str) -> bool:
    return re.match(email_pattern, email) is not None


email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.post("/usersignup")
async def create_user(usercreate: UserCreate, db: db_dependency):
    try:
        if not validate_email(usercreate.email):
            raise HTTPException(status_code=404, detail="invalid email format")
        
        new_user = models.User(
            username = usercreate.username,
            email = usercreate.email, 
            password = usercreate.password  
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return "success"
    except SQLAlchemyError as e:
        return "failed"
    
@app.post("/login")
async def user_login(userlogin: UserBase, db: db_dependency):
    pass

    
@app.post("/preferences")
async def set_preferences(preferences: PreferenceBase, db: db_dependency):
    try:

        preference = models.Preference(
            weather = preferences.weather,
            activity_type = preferences.activity_type,
            activity = preferences.activity,
            preference_score = preferences.preference_score
        )

        db.add(preference)
        db.commit()
        db.refresh(preference)

        return "success"
    except SQLAlchemyError as e:
        return "failed"
    
@app.get('/recomendation/', response_model=List[str])
def get_recomendation(db: db_dependency):
    activities = db.query(Preference).filter(
        Preference.weather == "sunny",
        Preference.activity_type == "outdoor",
        Preference.preference_score > 3,
        Preference.preference_score <= 5,
        Preference.user_id == None 
    ).all()

    return [activity.activity for activity in activities]

    













from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from models import Preference, Recommendation
import re
from schemas import RecommendationCreate, UserCreate, UserBase, PreferenceBase, PreferenceResponse
from sqlalchemy.exc import SQLAlchemyError
from api import fetch_weather_data
from datetime import datetime, timedelta


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
    
@app.post("/recomendation")
async def create_recomendation(recomendation: RecommendationCreate, db: db_dependency):
    try:
        recomend = models.Recommendation(
        weather = recomendation.weather,
        temperature = recomendation.temperature,
        humidity = recomendation.humidity,
        activity_type = recomendation.activity_type,
        activity = recomendation.activity
        )
        
        db.add(recomend)
        db.commit()
        db.refresh(recomend)

        return "success"
    except SQLAlchemyError as e:
        return "failed"


    
@app.get('/recomendation/{activity_type}/{city_name}', response_model=List[str])
def get_recomendation(activity_type: str,city_name: str, db: db_dependency):
    clouds = ["overcast clouds", "broken clouds", "scattered clouds"]
    print(activity_type)

    weather_data = fetch_weather_data(city_name)

    description = weather_data["description"]
    temp_celsius = weather_data["temp_ceslsius"]
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    sun_rise_time = weather_data["sun_rise_time"]
    sun_set_time = weather_data["sun_set_time"]

    if description in clouds:
        description = "cloud"

    activities1 = db.query(Recommendation).filter(
    Recommendation.weather == description,
    Recommendation.activity_type == activity_type,
    # Recommendation.temperature == temp_celsius,
    # Recommendation.humidity == humidity,   
    ).all()
    print(activities1)   
    



    recommended_activities_from_recommendations = [activity.activity for activity in activities1]
    print(recommended_activities_from_recommendations)

    activities2 = db.query(Preference).filter(
        Preference.weather == description,
        Preference.activity_type == activity_type,
        Preference.preference_score > 3,
        Preference.preference_score <= 5,
        Preference.user_id == None 
    ).all()

    recommended_activities_from_preferences = [activity.activity for activity in activities2]
    print(recommended_activities_from_preferences)

    recommended_activities_from_recommendations.extend(recommended_activities_from_preferences)

    if 15 < wind_speed < 25 and 20 < temp_celsius < 30 and description == "clear sky" and activity_type == "outdoor":
        recommended_activities_from_recommendations.extend(["Kiting"])
        recommended_activities_from_recommendations.extend(["Sailing"])

    
    current_time = datetime.now()

    if current_time >= sun_rise_time and current_time <= sun_rise_time + timedelta(hours=2):
        recommended_activities_from_recommendations.extend(["Early morning walk"])
    
    if current_time <= sun_set_time and current_time >= sun_set_time - timedelta(hours=2):
        recommended_activities_from_recommendations.extend(["Evening hikes"])
    
    recommendations = list(set(recommended_activities_from_recommendations))

    return recommendations



from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated, List, Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from models import Preference, Recommendation, User
import re
from schemas import RecommendationCreate, TokenData, UserCreate, UserBase, PreferenceBase, UserInDB, Token
from sqlalchemy.exc import SQLAlchemyError
from api import fetch_weather_data
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#email validator
def validate_email(email: str) -> bool:
    return re.match(email_pattern, email) is not None

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

#city_name validator
def validate_city_name(city_name: str) -> bool:
    return re.match(city_name_pattern, city_name) is not None

city_name_pattern = r'^[a-zA-Z\s-]+$'

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "d4df28b301f4518d2bdce68cb868e8e19340c4a059a3470232815bc52432d95b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt

@app.get("/")
def Home():
    return {"message":"Please provides /docs after the link on addres bar for documenation"}

@app.post("/usersignup")
async def create_user(user_create: UserCreate, db: db_dependency):
    try:
        db_user = get_user(db, username=user_create.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        if not validate_email(user_create.email):
            raise HTTPException(status_code=404, detail="invalid email format")
        
        hashed_password = get_password_hash(user_create.password)
        
        db_user = models.User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # Create token for the new user
        access_token = create_access_token(data={"sub": user_create.username})
        return {"access_token": access_token, "token_type": "bearer"}
        
        return "success"
    except SQLAlchemyError as e:
        return "failed"
    

@app.post("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}



async def get_current_user(token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW.Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

# user can submit their preferences to db through this endpoint
@app.post("/users/preferences")
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

# admin can store recomentations with respect to different parameters on this endpoint    
@app.post("/users/recomendation")
async def create_recomendation(recomendation: RecommendationCreate, db: db_dependency):
    try:
        recomend = models.Recommendation(
        weather = recomendation.weather,
        activity_type = recomendation.activity_type,
        activity = recomendation.activity
        )
        
        db.add(recomend)
        db.commit()
        db.refresh(recomend)

        return "success"
    except SQLAlchemyError as e:
        return "failed"


# User will get the recomentation of activites with respect to the properties or data that comes from the OpenWeather api and also with respect to user Preferences
@app.get('/users/recomendation/{activity_type}/{city_name}', response_model=List[str])
async def get_recomendation(activity_type: str,city_name: str, db: db_dependency):
    try:
        if not validate_city_name(city_name):
            raise HTTPException(status_code=404, detail="unknown city")
        
        weather_data = fetch_weather_data(city_name)

        description = weather_data["description"]
        temp_celsius = weather_data["temp_ceslsius"]
        humidity = weather_data["humidity"]
        wind_speed = weather_data["wind_speed"]
        sun_rise_time = weather_data["sun_rise_time"]
        sun_set_time = weather_data["sun_set_time"]

        clouds = ["overcast clouds", "broken clouds", "scattered clouds"]

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
    except SQLAlchemyError as e:
        return {"recomendation failed"}

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}









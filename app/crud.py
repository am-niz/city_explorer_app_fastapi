from main import db_dependency
from schemas import UserCreate
from sqlalchemy.exc import SQLAlchemyError
import models

# def get_user_preferences(db: db_dependency, user_id: int):
#     return db.query(models.Preference).filter(models.Preference.user_id == user_id).all()




from sqlalchemy import create_engine  #mange teh connection to database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:admin@localhost:5432/city_explorer_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind= engine)

Base = declarative_base()
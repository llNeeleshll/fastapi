from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_db_url = "sqlite:///./todos.db"

engine = create_engine(sqlalchemy_db_url, connect_args={"check_same_thread" : False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


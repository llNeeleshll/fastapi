from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy_db_url = "sqlite:///./todos.db"
sqlalchemy_db_url = "postgresql://postgres:postgres@localhost/TodoApplicationDatabase"

engine = create_engine(sqlalchemy_db_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


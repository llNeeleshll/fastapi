from turtle import stamp
from fastapi import FastAPI, Depends, HTTPException, Request, status, Header
from pydantic import BaseModel, Field
from typing import Optional
import models
import uvicorn
from passlib.context import CryptContext
from database import engine, session_local
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "Monika"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engine)

def get_session():
    try:
        session = session_local()
        yield session
    finally:
        session.close()

class CreateUser(BaseModel):
    username: str = Field()
    email : str = Field()
    first_name: str = Field()
    last_name: str = Field()
    password: str = Field()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(password: str, hashed_password: str):
    return bcrypt_context.verify(password, hashed_password)

def authenticate_user(username:str, password:str, session: Session):
    logged_in_user = session.query(models.User).filter(models.User.user_name == username).first()

    if logged_in_user is None:
        return False

    if not verify_password(password, logged_in_user.hashed_password):
        return False

    return logged_in_user

def create_access_token(username:str, user_id:int, expires_delta = Optional[timedelta]):

    encode = { "sub" : username, "id" : user_id }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    encode.update({"exp" :  expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_currrent_user(token:str = Depends(oauth2_bearer)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id : int = payload.get("id")

        if user_id is None or username is None:
            raise get_user_exception()
        
        return {
            "username": username,
            "user id": user_id
        }

    except JWTError:
        raise get_user_exception()

@app.post("/createuser")
async def create_user(user: CreateUser, session: Session = Depends(get_session)):
    create_user_new = models.User()

    create_user_new.email = user.email
    create_user_new.user_name = user.username
    create_user_new.first_name = user.first_name
    create_user_new.last_name = user.last_name
    hashed_password = bcrypt_context.hash(user.password)
    create_user_new.hashed_password = hashed_password
    create_user_new.is_active = True

    session.add(create_user_new)
    session.commit()

    return {
        "message" : "Success"
    }

@app.post("/token")
async def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(), session : Session = Depends(get_session)):
    user  = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=404, detail="User is invalid")

    token_expires = timedelta(minutes=20)
    token =  create_access_token(user.user_name, user.id, token_expires)

    return {"token" : token}

def get_user_exception():

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid Credentials",
        headers={"WWW=Authenticate" : "Bearer"})

    return credential_exception

def token_exception():
    
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username and password",
        headers={"WWW=Authenticate" : "Bearer"})

    return token_exception

if __name__ == "__main__":
    uvicorn.run("auth:app", host='0.0.0.0', port=9000, reload=True)
import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, Request, status, APIRouter
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
from .auth import get_currrent_user, get_user_exception

class UserPassword(BaseModel):
    currentpassword: str
    newpassword: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    try:
        session = session_local()
        yield session
    finally:
        session.close()


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/getusers")
async def create_user(session: Session = Depends(get_session)):
    return session.query(models.Users).all()

@router.post("/getusersbyusername/{username}")
async def create_user(username:str, session: Session = Depends(get_session)):
    return session.query(models.Users).filter(models.Users.user_name == username).first()

@router.post("/changepassword/")
async def create_user(user_password:UserPassword, user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):

    if not user:
        return get_user_exception()

    user_context = session.query(models.Users).filter(models.Users.id == user.get('user id')).first()

    if not user_context:
        return HTTPException(status_code=404, detail="No user with that username")

    if bcrypt_context.verify(user_password.currentpassword, user_context.hashed_password):
        hashed_password = bcrypt_context.hash(user_password.newpassword)
        user_context.hashed_password = hashed_password
        session.commit()

        return {
            "message" : "Password Changed"
        }

    else:
        return{
            "message" : "Password doesn't match"
        }


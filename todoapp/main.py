from os import stat
from fastapi import FastAPI, Depends
import models
from database import engine, session_local
import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Request, status, Header
import helper_models.todos as td
from routers.auth import get_currrent_user, get_user_exception
from routers import auth, todos, users
from company import companyapis, dependencies

app = FastAPI()

# Include all the routers
app.include_router(auth.auth_router)
app.include_router(todos.todo_router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["Company APIS"],
    responses={418: {"description" : "Internal Use Only" }},
    dependencies=[Depends(dependencies.get_token_header)]
    )
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
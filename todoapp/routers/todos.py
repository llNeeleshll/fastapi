import sys
sys.path.append("..")

from os import stat
from fastapi import APIRouter, Depends
import models
from database import engine, session_local
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, status, Header
import helper_models.todos as td
from .auth import get_currrent_user, get_user_exception

todo_router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

def get_session():
    try:
        session = session_local()
        yield session
    finally:
        session.close()

@todo_router.get("/readall")
def read_all(session: Session = Depends(get_session)):
    return session.query(models.Todo).all()

@todo_router.get("/")
async def get_todos_by_id(todo_id: int, user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):

    if not user:
        return get_user_exception()

    todo = session.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.get('user id')).first()

    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Not Found")

@todo_router.get("/byuser")
async def get_todos_by_user(user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):
    if not user:
        return get_user_exception()
    else:
        return session.query(models.Todo).filter(models.Todo.user_id == user.get('user id')).all()

@todo_router.post("/create")
async def create_todo(todo: td.Todo, user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):

    if not user:
        return get_user_exception()

    new_todo = models.Todo()
    new_todo.title = todo.title
    new_todo.description = todo.description
    new_todo.priority = todo.priority
    new_todo.complete = todo.complete
    new_todo.user_id = user.get("user id")

    session.add(new_todo)
    session.commit()
    
    return {
        "status" : 201,
        "transaction" : "Success"
    }

@todo_router.put("/update/{todo_id}")
async def update_todo(todo_id : int, todo: td.Todo, user: dict = Depends(get_currrent_user), session : Session = Depends(get_session)):
        
    if not user:
        return get_user_exception()

    todo_edit = session.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.get('user id')).first()

    if todo_edit is not None:
        todo_edit.title = todo.title
        todo_edit.decription = todo.description
        todo_edit.priority = todo.priority
        todo_edit.complete = todo.complete

        session.commit()

        return {
            "status" : 200,
            "transaction" : "Success"
        }
    else:
        raise HTTPException(status_code=404, detail="Todo Not Found")

@todo_router.delete("/deletetodo/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):

    if not user:
        return get_user_exception()

    todo_delete = session.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.get('user id')).first()

    if todo_delete is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    session.delete(todo_delete)
    session.commit()

    return {
            "status" : 200,
            "transaction" : "Success"
        }

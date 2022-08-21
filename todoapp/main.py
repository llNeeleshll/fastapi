from os import stat
from fastapi import FastAPI, Depends
import models
from database import engine, session_local
import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Request, status, Header
import helper_models.todos as td
from auth import get_currrent_user, get_user_exception

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_session():
    try:
        session = session_local()
        yield session
    finally:
        session.close()

@app.get("/readall")
def read_all(session: Session = Depends(get_session)):
    return session.query(models.Todo).all()

@app.get("/todo")
async def get_todos_by_id(todo_id: int, user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):

    if not user:
        return get_user_exception()

    todo = session.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.user_id == user.get('user id')).first()

    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Not Found")

@app.get("/todobyuser")
async def get_todos_by_user(user: dict = Depends(get_currrent_user), session: Session = Depends(get_session)):
    if not user:
        return get_user_exception()
    else:
        return session.query(models.Todo).filter(models.Todo.user_id == user.get('user id')).all()

@app.post("/createtodo")
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

@app.put("/updatetodo/{todo_id}")
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

@app.delete("/deletetodo/{todo_id}")
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


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
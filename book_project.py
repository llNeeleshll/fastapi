import enum
from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from pydantic import BaseModel, Field
from uuid import UUID
import random
from starlette.responses import JSONResponse

class NegativeNumberException(Exception):
    def __init__(self, no_of_books):
        self.no_of_books = no_of_books

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] =  Field(title="Description of Book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=5)

    class Config:
        schema_extra = {
            "example" : {
                "id" : "Some UUID Value",
                "title" : "Enter the Book title",
                "Author" : "Who wrote the book?",
                "Description" : "Describe about the book.",
                "rating" : "Book Rating"
            }
        }


app = FastAPI()

books = []

@app.exception_handler(NegativeNumberException)
async def neagtive_number_exception(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message" : f"Why do you need {exception.no_of_books} to be negative?"})

@app.get("/getbooks")
async def read_all_books(no_of_books : Optional[int] = None):
    fill_books()

    if no_of_books is not None and no_of_books < 0:
        raise NegativeNumberException(no_of_books=no_of_books)

    if no_of_books is not None and no_of_books > 0:
        return books[0:no_of_books]

    return books

@app.get("/book/{book_id}")
async def get_book_by_id(book_id: UUID):
    for item in books:
        if item.id == book_id:
            return item

@app.post("/createbook")
async def create_book(book: Book):
    books.append(book)

@app.put("/updatebook")
async def update_book(book_id : UUID, book : Book):

    for i, item in enumerate(books):
        if item.id == book_id:
            books[i] = book
            return book

@app.delete("/deletebook")
async def delete_book(book_id : UUID):
    for i, item in enumerate(books):
        if item.id == book_id:
            del books[i]
            return

    raise HTTPException(status_code=404, detail="Book Not Found", headers={"X-Header-Error" : "Nothing to be seen at the UUID"})

def fill_books():
    for i in range(0,10):
        books.append(Book(id=uuid.uuid4(),
        title='book_' + str(i),
        author='Author_' + str(i),
        description="Some Book " + str(i) + " description",
        rating=random.randint(0, 4)))
    

if __name__ == "__main__":
    uvicorn.run("book_project:app", host='0.0.0.0', port=8000, reload=True)
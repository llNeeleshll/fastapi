from typing import Optional
from unittest import async_case
from fastapi import FastAPI
from enum import Enum
import uvicorn

app = FastAPI()

books = {
    "book_1" : {"title" : "Title One", 'author' : "Author One"},
    "book_2" : {"title" : "Title Two", 'author' : "Author Two"},
    "book_3" : {"title" : "Title Three", 'author' : "Author Three"},
    "book_4" : {"title" : "Title Four", 'author' : "Author Four"},
    "book_5" : {"title" : "Title Five", 'author' : "Author Five"}
}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = books.copy()
        del new_books[skip_book]
        return new_books
    else:
        return books

@app.get("/directions/{direction_name}")
def get_directions(direction_name : DirectionName):
    return {"message" : "This"}

@app.get("/book/mybook")
def read_fav_book():
    return {"book_title" : "My Book"}


@app.get("/book/{book_id}")
def read_book(book_id: int):
    return {"book_title" : book_id}

@app.post("/create_book")
def create_book(book_title, book_author):

    current_book_id = 0

    if len(books) > 0:

        for book in books:
            current_book_id = int(book.split('_')[-1])
            
        books['book_' + str(current_book_id + 1)] = {"title" : book_title, "author" : book_author}
    
    return books['book_' + str(current_book_id + 1)]


@app.put("/update_book/{book_name}")
def update_book(book_name: str, book_title: str, book_author: str):
    books[book_name] = {"title": book_title, "author": book_author}
    return books[book_name]

@app.delete("/delete_book/{book_name}")
def delete_book(book_name: str):
    del books[book_name]
    return f'{book_name} deleted'



if __name__ == "__main__":
    uvicorn.run("books:app", host='0.0.0.0', port=8000, reload=True)
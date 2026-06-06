from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

books = [
{
    "id" : 1,
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "publish_date": "1988-01-01"
},
{
    "id" : 2,
    "title": "The God of Small Things",
    "author": "Arundhati Roy",
    "publish_date": "1997-04-04"
},
{
    "id": 3,
    "title": "The White Tiger",
    "author": "Aravind Adiga",
    "publish_date": "2008-01-01"
},
{
    "id" : 4,
    "title": "The Palace of Illusions",
    "author": "Chitra Banerjee Divakaruni",
    "publish_date": "2008-02-12"
}]

app = FastAPI()

@app.get("/books")
def get_all_book():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail="Book not found")

class Book(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str

@app.post("/book",status_code=status.HTTP_201_CREATED)

def create_book(book:Book):
    new_book = book.model_dump
    books.append(new_book)
    return new_book

class UpdateBook(BaseModel):
    title:int
    author:str
    publish_date:str

@app.put("/book/{book_id}")
def update_book(book_id: int, update_book:UpdateBook):
    for book in books:
        if book["id"] == book_id:
            book["title"] = update_book.title
            book["author"] = update_book.author
            book["publish_date"] = update_book.publish_date
            return book
        raise HTTPException(status_code=HTTP__NOT_FOUND, detail="Books not found")
    
@app.delete("/book/{book_id}")
def delete(book_id:int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"Message: Our book deteted"}
    raise HTTPException(status_code=HTTP__NOT_FOUND, detail="Books not found")


    

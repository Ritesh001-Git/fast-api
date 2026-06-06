from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date
from database import getDB
import model

app = FastAPI()


class BookCreate(BaseModel):
    title: str
    author: str
    publish_date: date


@app.post("/books")
def create_book(
    book: BookCreate,
    db: Session = Depends(getDB)
):
    new_book = model.Book(
        title=book.title,
        author=book.author,
        publish_date=book.publish_date
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.get("/books")
def get_books(
    db: Session = Depends(getDB)
):
    books = db.query(model.Book).all()
    return books
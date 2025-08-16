from fastapi import FastAPI, HTTPException
from typing import List
from library import Library
from models import BookModel, ISBNModel

app = FastAPI(title="Kütüphane API")

lib = Library()

@app.get("/books", response_model=List[BookModel])
def get_books():
    return [BookModel(title=b.title, author=b.author, isbn=b.isbn, type=b.type) for b in lib.books]

@app.post("/books", response_model=BookModel)
def add_book(book_data: ISBNModel):
    book = lib.add_book_by_isbn(book_data.isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya zaten mevcut.")
    return BookModel(title=book.title, author=book.author, isbn=book.isbn, type=book.type)

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    book = lib.remove_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return {"detail": f"{book.title} başarıyla silindi."}

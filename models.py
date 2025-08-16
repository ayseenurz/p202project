from pydantic import BaseModel

class BookModel(BaseModel):
    title: str
    author: str
    isbn: str
    type: str = "Book"

class ISBNModel(BaseModel):
    isbn: str

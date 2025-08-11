import json
import os


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_dict(self):
        return {
            "type": "Book",
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
        }


class Ebook(Book):
    def __init__(self, title, author, isbn, file_type):
        super().__init__(title, author, isbn)
        self.type = file_type

    def to_dict(self):
        return {
            "type": "Ebook",
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "file_type": self.type,
        }


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    data = json.load(f)
                    self.books = []
                    for b in data:
                        book_type = b.get("type", "Book")
                        if book_type == "Book":
                            self.books.append(Book(b["title"], b["author"], b["isbn"]))
                        elif book_type == "Ebook":
                            self.books.append(
                                Ebook(
                                    b["title"],
                                    b["author"],
                                    b["isbn"],
                                    b.get("file_type", ""),
                                )
                            )
                except json.JSONDecodeError:
                  self.books = []

    def save_books(self):
        with open(self.filename, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def remove_books(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]
        self.save_books()

    def list_books(self):
        if not self.books:
            print("Kütüphanede kitap yok.")
        else:
            for b in self.books:
                if isinstance(b, Ebook):
                    print(f"[EBOOK] {b.title} by {b.author} ({b.type}) - ISBN: {b.isbn}")
                else:
                    print(f"{b.title} by {b.author} - ISBN: {b.isbn}")

    def find_book(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

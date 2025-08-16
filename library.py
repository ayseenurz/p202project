import json
import os
import httpx

class Book:
    def __init__(self, title, author, isbn, type="Book"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.type = type

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "type": self.type,
        }

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.books = [Book(**b) for b in data]
            except json.JSONDecodeError:
                self.books = []

    def save_books(self):
        with open(self.filename, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def find_book(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def get_author_name(self, client, author_key):
        author_url = f"https://openlibrary.org{author_key}.json"
        response = client.get(author_url)
        if response.status_code == 200:
            return response.json().get("name", "Bilinmeyen Yazar")
        return "Bilinmeyen Yazar"

    def add_book_by_isbn(self, isbn):
        if self.find_book(isbn):
            return None  

        try:
            with httpx.Client(follow_redirects=True, timeout=10) as client:
                url = f"https://openlibrary.org/isbn/{isbn}.json"
                res = client.get(url)

                if res.status_code == 404:
                    return None

                res.raise_for_status()
                data = res.json()
                title = data.get("title", "Bilinmeyen")

                authors = [
                    self.get_author_name(client, a.get("key"))
                    for a in data.get("authors", []) if a.get("key")
                ]
                author_names = ", ".join(authors) if authors else "Bilinmeyen Yazar"

                book = Book(title, author_names, isbn)
                self.books.append(book)
                self.save_books()
                return book

        except Exception:
            return None

    def remove_book(self, isbn):
        book = self.find_book(isbn)
        if book:
            self.books = [b for b in self.books if b.isbn != isbn]
            self.save_books()
            return book
        return None

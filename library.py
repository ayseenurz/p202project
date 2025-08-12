import json
import os
import httpx


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

    def add_book_by_isbn(self, isbn):
        try:
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url, timeout=10)

            if response.status_code == 404:
                print("Kitap bulunamadı.")
                return  # Burada fonksiyon sonlanmalı

            response.raise_for_status()
            data = response.json()

            title = data.get("title", "Bilinmiyor")

            authors = []
            for author in data.get("authors", []):
                author_key = author.get("key")
                if author_key:
                    author_url = f"https://openlibrary.org{author_key}.json"
                    with httpx.Client(follow_redirects=True) as client:
                        author_res = client.get(author_url)
                    if author_res.status_code == 200:
                        author_data = author_res.json()
                        authors.append(author_data.get("name", "Bilinmeyen Yazar"))

            author_names = ", ".join(authors) if authors else "Bilinmeyen Yazar"

            book = Book(title, author_names, isbn)
            self.books.append(book)     # Burada doğrudan listeye ekliyoruz
            self.save_books()           # Kitap eklendiğinde dosyaya kaydet
            print(f"Kitap eklendi: {title}")

        except httpx.RequestError:
            print("İnternet bağlantısı yok veya API'ye ulaşılamıyor.")
        except Exception as e:
            print("Bir hata oluştu:", e)

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


def main():
    lib = Library()

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        secim = input("Seçiminizi yapın: ")

        if secim == "1":
            isbn = input("ISBN girin: ")
            lib.add_book_by_isbn(isbn)

        elif secim == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN'i: ")
            book = lib.find_book(isbn)
            if book:
                lib.remove_books(isbn)
                print("Kitap silindi.")
            else:
                print("Bu ISBN ile kayıtlı kitap bulunamadı.")

        elif secim == "3":
            lib.list_books()

        elif secim == "4":
            isbn = input("Aramak istediğiniz kitabın ISBN'i: ")
            book = lib.find_book(isbn)
            if book:
                if isinstance(book, Ebook):
                    print(f"[EBOOK] {book.title} by {book.author} ({book.type})")
                else:
                    print(f"{book.title} by {book.author}")
            else:
                print("Kitap bulunamadı.")

        elif secim == "5":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim. Tekrar deneyin.")


if __name__ == "__main__":
    main()

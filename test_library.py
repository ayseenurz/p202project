import os
import json
import pytest
from library import Book, Ebook, Library

TEST_FILE = "test_library.json"


@pytest.fixture
def empty_library():
    # Eğer varsa test dosyasını sil, temiz başla
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    lib = Library(filename=TEST_FILE)
    lib.books = []
    return lib


def test_add_book(empty_library):
    lib = empty_library
    book = Book("Test Book", "Test Author", "12345")
    lib.add_book(book)

    # Kitap listesine eklenmiş mi?
    assert len(lib.books) == 1
    assert lib.books[0].title == "Test Book"

    # JSON dosyasında var mı?
    with open(TEST_FILE, "r") as f:
        data = json.load(f)
    assert data[0]["title"] == "Test Book"


def test_remove_book(empty_library):
    lib = empty_library
    book = Book("Book to Remove", "Author", "11111")
    lib.add_book(book)

    lib.remove_books("11111")

    # Artık bulunmamalı
    assert lib.find_book("11111") is None
    assert len(lib.books) == 0


def test_find_book(empty_library):
    lib = empty_library
    book = Ebook("Ebook Title", "Ebook Author", "22222", "PDF")
    lib.add_book(book)

    found = lib.find_book("22222")
    assert found is not None
    assert isinstance(found, Ebook)
    assert found.type == "PDF"


def test_list_books_output(empty_library, capsys):
    lib = empty_library
    lib.add_book(Book("A", "B", "33333"))
    lib.list_books()

    captured = capsys.readouterr()
    assert "A by B" in captured.out

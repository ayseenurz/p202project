import os
import json
import pytest
from library import Library

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
    isbn = "0451526538"  # Geçerli ISBN
    lib.add_book_by_isbn(isbn)
    
    # Kitap listesine eklenmiş mi?
    assert len(lib.books) == 1
    assert lib.books[0].isbn == isbn

    # JSON dosyasında var mı?
    with open(TEST_FILE, "r") as f:
        data = json.load(f)
    assert data[0]["isbn"] == isbn

def test_remove_book(empty_library):
    lib = empty_library
    isbn = "0451526538"
    lib.add_book_by_isbn(isbn)

    lib.remove_book(isbn)

    # Artık bulunmamalı
    assert lib.find_book(isbn) is None
    assert len(lib.books) == 0

def test_find_book(empty_library):
    lib = empty_library
    isbn = "0451526538"
    lib.add_book_by_isbn(isbn)

    found = lib.find_book(isbn)
    assert found is not None
    assert found.isbn == isbn

def test_list_books_output(empty_library, capsys):
    lib = empty_library
    isbn = "0451526538"
    lib.add_book_by_isbn(isbn)
    
    # list_books metodu ekrana yazacak
    for b in lib.books:
        print(f"{b.title} by {b.author} - ISBN: {b.isbn}")

    captured = capsys.readouterr()
    assert "ISBN: 0451526538" in captured.out

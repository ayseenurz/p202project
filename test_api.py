import pytest
from fastapi.testclient import TestClient
from api import app  # api.py dosyanızın adı
from library import Library

client = TestClient(app)

@pytest.fixture
def setup_library():
    # Testler için Library örneği temizlenebilir
    lib = Library()
    lib.books = []
    return lib

def test_get_books_empty(setup_library):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book_valid_isbn(setup_library):
    isbn = "0451526538"  # Geçerli ISBN
    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == isbn
    assert "title" in data
    assert "author" in data

def test_add_book_invalid_isbn(setup_library):
    isbn = "0000000000"  # Geçersiz ISBN
    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı veya zaten mevcut."

def test_delete_book(setup_library):
    isbn = "0451526538"  # Geçerli ISBN
    # Önce ekle
    client.post("/books", json={"isbn": isbn})
    
    # Şimdi sil
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 200
    assert f"{isbn}" not in str([b["isbn"] for b in setup_library.books])

def test_delete_book_not_found(setup_library):
    isbn = "0000000000"
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı."

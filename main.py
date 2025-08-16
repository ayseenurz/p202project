from library import Library

lib = Library()

while True:
    print("\n--- Kütüphane Menüsü ---")
    print("1. Kitap Ekle (ISBN ile)")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Kitap Ara (ISBN ile)")
    print("5. Çıkış")

    secim = input("Seçiminizi yapın: ")

    if secim == "1":
        isbn = input("ISBN girin: ")
        book = lib.add_book_by_isbn(isbn)
        if book:
            print(f"Kitap eklendi: {book.title} by {book.author}")
        else:
            print("Kitap bulunamadı veya zaten mevcut.")

    elif secim == "2":
        isbn = input("Silmek istediğiniz kitabın ISBN'i: ")
        book = lib.remove_book(isbn)
        if book:
            print(f"{book.title} silindi.")
        else:
            print("Kitap bulunamadı.")

    elif secim == "3":
        if not lib.books:
            print("Kütüphanede kitap yok.")
        else:
            for b in lib.books:
                print(f"{b.title} by {b.author} - ISBN: {b.isbn}")

    elif secim == "4":
        isbn = input("Aramak istediğiniz kitabın ISBN'i: ")
        book = lib.find_book(isbn)
        if book:
            print(f"{book.title} by {book.author}")
        else:
            print("Kitap bulunamadı.")

    elif secim == "5":
        print("Çıkılıyor...")
        break

    else:
        print("Geçersiz seçim.")

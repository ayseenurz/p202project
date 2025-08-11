from library import Book, Ebook, Library


def main():
    lib = Library()

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        secim = input("Seçiminizi yapın: ")

        if secim == "1":
            title = input("Kitap adı: ")
            author = input("Yazar: ")
            isbn = input("ISBN: ")
            kitap_tipi = input("Ebook mu? (e/h): ").lower()

            if kitap_tipi == "e":
                file_type = input("Dosya tipi (PDF, EPUB vs.): ")
                book = Ebook(title, author, isbn, file_type)
            else:
                book = Book(title, author, isbn)

            lib.add_book(book)
            print("Kitap eklendi.")

        elif secim == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN'i: ")
            lib.remove_books(isbn)
            print("Kitap silindi.")

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

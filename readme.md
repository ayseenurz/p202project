# Kütüphane Yönetim Projesi

Bu proje, Python 202 Bootcamp kapsamında geliştirilmiş bir **Kütüphane Yönetim Uygulamasıdır**. Proje ile hem terminal üzerinden hem de web API üzerinden kitapları yönetebilirsiniz.

---

## Kurulum

Projeyi klonlayın ve gerekli bağımlılıkları yükleyin:

```bash
git clone https://github.com/kullaniciadi/proje-adi.git
cd proje-adi
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Kullanım

### Terminal Uygulaması

```bash
python main.py
```

- Kitap ekle (ISBN ile), sil, listele, ara.
- ISBN girildiğinde Open Library API’den otomatik bilgi çekilir.

### API Sunucusu

```bash
uvicorn api:app --reload
```

- Tarayıcı veya Postman ile: `http://127.0.0.1:8000/docs`
- Endpointler:
  - `GET /books` → Tüm kitapları listeler
  - `POST /books` → Yeni kitap ekler (`{"isbn": "9780451526538"}`)
  - `DELETE /books/{isbn}` → Kitap siler

---

## Testler

```bash
pytest
```

- `test_library.py` → Library sınıfı testleri
- `test_api.py` → API testleri


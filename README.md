# Biblioteka Książek - Aplikacja Flask

Prosta aplikacja webowa do zarządzania kolekcją książek, zbudowana przy użyciu frameworka Flask i biblioteki Flask-WTF. Aplikacja pozwala na przeglądanie, dodawanie, edytowanie i usuwanie książek, a dane przechowuje w pliku `books.json`. Obsługuje także przesyłanie okładek oraz pobieranie danych książki po numerze ISBN z serwisu e-isbn.pl.

## Funkcjonalności

- Wyświetlanie listy książek w przejrzystej tabeli.
- Dodawanie nowych książek za pomocą formularza z walidacją po stronie serwera.
- Edycja danych istniejących książek.
- Usuwanie książek.
- Przesyłanie okładek książek (obsługa plików jpg/png/jpeg).
- Utrwalanie danych w pliku `books.json`.
- Nowoczesny i responsywny interfejs użytkownika.
- REST API do zarządzania książkami (GET, POST, PUT, DELETE).
- Endpoint do pobierania danych książki po numerze ISBN (ONIX z e-isbn.pl).

## Technologie

- **Backend:** Python, Flask
- **Formularze:** Flask-WTF, WTForms
- **Frontend:** HTML5, CSS3, Jinja2
- **API:** REST, JSON

## Instalacja i uruchomienie

Aby uruchomić aplikację lokalnie, postępuj zgodnie z poniższymi krokami.

1.  **Sklonuj repozytorium** (lub pobierz pliki projektu):
    ```bash
    git clone https://github.com/MarcinSachs/kodilla_biblioteka_wtf.git
    cd kodilla_biblioteka_wtf
    ```

2.  **Utwórz i aktywuj wirtualne środowisko:**
    ```bash
    # Utwórz środowisko
    python -m venv .venv

    # Aktywuj na Windows
    .venv\Scripts\activate

    # Aktywuj na macOS/Linux
    source .venv/bin/activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uruchom aplikację:**
    ```bash
    python app.py
    ```

5.  **Otwórz aplikację w przeglądarce:**
    Przejdź pod adres http://127.0.0.1:5000/books/

## Struktura plików

```
kodilla_biblioteka_wtf/
├── static/
│   └── uploads/          # Przesłane okładki książek
│   └── style.css         # Style CSS
├── templates/
│   ├── books.html        # Szablon listy książek
│   ├── book_add.html     # Szablon dodawania książki
│   └── book_edit.html    # Szablon edycji książki
├── .venv/                # Środowisko wirtualne
├── app.py                # Główny plik aplikacji Flask
├── books.json            # Plik z danymi książek
├── forms.py              # Definicje formularzy WTForms
├── models.py             # Model do zarządzania danymi
└── requirements.txt      # Zależności projektu
```

## API

- **GET** `/books/api/v1/books/` – lista książek (JSON)
- **GET** `/books/api/v1/books/<id>` – szczegóły książki
- **POST** `/books/api/v1/books/` – dodaj książkę (JSON)
- **PUT** `/books/api/v1/books/<id>` – edytuj książkę (JSON)
- **DELETE** `/books/api/v1/books/<id>` – usuń książkę
- **GET** `/api/v1/isbn/<isbn>` – pobierz dane książki po numerze ISBN

## Uwagi

- Okładki książek są zapisywane w katalogu `static/uploads/`.
- Plik `books.json` jest tworzony automatycznie przy pierwszym uruchomieniu, jeśli nie istnieje.
- W przypadku korzystania z API, wymagane jest przesyłanie danych w formacie JSON.

---
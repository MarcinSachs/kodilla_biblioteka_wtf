# Biblioteka Książek - Aplikacja Flask

Prosta aplikacja webowa do zarządzania kolekcją książek, zbudowana przy użyciu frameworka Flask i biblioteki Flask-WTF. Aplikacja pozwala na przeglądanie, dodawanie i edytowanie książek, a dane przechowuje w pliku `books.json`.


## Funkcjonalności

- Wyświetlanie listy książek w przejrzystej tabeli.
- Dodawanie nowych książek za pomocą formularza z walidacją po stronie serwera.
- Edycja danych istniejących książek.
- Utrwalanie danych w pliku `books.json`.
- Nowoczesny i responsywny interfejs użytkownika z ikonami.

## Technologie

- **Backend:** Python, Flask
- **Formularze:** Flask-WTF, WTForms
- **Frontend:** HTML5, CSS3, Jinja2
- **Ikony:** Font Awesome

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
    flask run
    ```
    Alternatywnie, możesz uruchomić bezpośrednio plik `app.py`:
    ```bash
    python app.py
    ```

5.  **Otwórz aplikację w przeglądarce:**
    Przejdź pod adres http://127.0.0.1:5000/library/

## Struktura plików

```
kodilla_biblioteka_wtf/
├── static/
│   └── style.css         # Style CSS
├── templates/
│   ├── book.html         # Szablon edycji książki
│   └── library.html      # Główny szablon listy i dodawania
├── .venv/                # Środowisko wirtualne
├── app.py                # Główny plik aplikacji Flask
├── books.json            # Plik z danymi książek
├── forms.py              # Definicje formularzy WTForms
├── models.py             # Model do zarządzania danymi
└── requirements.txt      # Zależności projektu
```
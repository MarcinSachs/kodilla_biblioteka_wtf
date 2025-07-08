from flask import Flask, render_template, redirect, url_for, abort, flash, jsonify, make_response, request
from forms import BookForm
from models import books
import os
from werkzeug.utils import secure_filename
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/books/", methods=["GET"])
def library():
    return render_template("books.html", books=books.all())


@app.route("/books/add/", methods=["GET", "POST"])
def book_add():
    form = BookForm()
    genres = [genre[0] for genre in books.get_unique_genres()]
    if form.validate_on_submit():
        new_book_data = {
            'title': form.title.data,
            'author': form.author.data,
            'genre': form.genre.data,
            'year': form.year.data
        }

        if form.cover.data:
            f = form.cover.data
            cover_filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
            new_book_data['cover'] = cover_filename

        books.create(new_book_data)
        flash("Książka została pomyślnie dodana!", "success")
        return redirect(url_for("library"))

    return render_template("book_add.html", form=form, genres=genres)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_edit(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)

    form = BookForm(data=book)

    genres = [genre[0] for genre in books.get_unique_genres()]
    if form.validate_on_submit():
        updated_data = {
            'title': form.title.data,
            'author': form.author.data,
            'genre': form.genre.data,
            'year': form.year.data,
            'cover': book.get('cover')
        }
        if form.cover.data:
            f = form.cover.data
            cover_filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
            updated_data['cover'] = cover_filename

        books.update(book_id, updated_data)
        flash("Dane książki zostały zaktualizowane.", "success")
        return redirect(url_for("library"))
    return render_template("book_edit.html", form=form, book_id=book_id, book=book, genres=genres)

# API


@app.route("/books/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())


@app.route("/books/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/books/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json:
        abort(400)
    required_fields = ['title', 'author', 'genre', 'year']
    if not all(field in request.json for field in required_fields):
        abort(400)
    if not isinstance(request.json.get('year'), int):
        abort(400)
    book_data = {
        'title': request.json['title'],
        'author': request.json['author'],
        'genre': request.json['genre'],
        'year': request.json['year'],
        'cover': request.json.get('cover', ""),
    }
    books.create(book_data)
    return jsonify({'book': book_data}), 201


@app.route("/books/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/books/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json

    type_checks = {'title': str, 'author': str,
                   'genre': str, 'year': int, 'cover': str}
    for field, expected_type in type_checks.items():
        if field in data and not isinstance(data[field], expected_type):
            abort(400)

    updated_book_data = {
        'id': book_id,
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'genre': data.get('genre', book['genre']),
        'year': data.get('year', book['year']),
        'cover': data.get('cover', book['cover'])
    }
    books.update(book_id, updated_book_data)
    return jsonify({'book': updated_book_data})

# Endpoint do pobierania danych po numerze ISBN


@app.route("/api/v1/isbn/<isbn>", methods=["GET"])
def get_book_by_isbn(isbn):
    """Pobiera dane książki z serwisu e-isbn.pl w formacie ONIX."""
    url = f"https://e-isbn.pl/IsbnWeb/api.xml?isbn={isbn}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Nie udało się połączyć z serwisem ISBN.", "details": str(e)}), 502

    try:
        # Definiujemy przestrzeń nazw dla formatu ONIX 3.0, która jest niezbędna do parsowania
        ns = {'onix': 'http://ns.editeur.org/onix/3.0/reference'}
        root = ET.fromstring(response.content)

        # Pobranie głównego elementu <Product> w przestrzeni nazw ONIX
        product = root.find('onix:Product', ns)
        if product is None:
            return jsonify({"error": "Nie znaleziono książki dla podanego numeru ISBN."}), 404

        # Wyciąganie tekstu z zagnieżdżonych elementów
        def find_text(element, path, namespace):
            node = element.find(path, namespace)
            return node.text if node is not None else None

        title = find_text(
            product, 'onix:DescriptiveDetail/onix:TitleDetail/onix:TitleElement/onix:TitleText', ns)

        # Autor jest w formacie "Nazwisko, Imię", więc go odwracamy
        author_inverted = find_text(
            product, "onix:DescriptiveDetail/onix:Contributor[onix:ContributorRole='A01']/onix:PersonNameInverted", ns)
        author = ''
        if author_inverted:
            parts = author_inverted.split(',', 1)
            author = f"{parts[1].strip()} {parts[0].strip()}" if len(
                parts) == 2 else author_inverted

        # Rok publikacji
        pub_date_node = product.find(
            "onix:PublishingDetail/onix:PublishingDate[onix:PublishingDateRole='01']/onix:Date", ns)
        year = int(pub_date_node.text[:4]) if pub_date_node is not None and pub_date_node.text and len(
            pub_date_node.text) >= 4 else None

        book_data = {
            'title': title or '',
            'author': author or '',
            'year': year,
        }

        return jsonify(book_data)
    except (ET.ParseError, AttributeError, TypeError) as e:
        # Obsługa błędów parsowania XML lub brakujących tagów
        return jsonify({"error": "Nie udało się przetworzyć danych z serwisu ISBN.", "details": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)

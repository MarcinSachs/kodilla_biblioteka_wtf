from flask import Flask, render_template, redirect, url_for, abort, flash, jsonify, make_response, request
from forms import BookForm
from models import books
import os
from werkzeug.utils import secure_filename

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)

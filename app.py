from flask import Flask, render_template, redirect, url_for, abort, flash
from forms import BookForm
from models import books
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/library/", methods=["GET", "POST"])
def library():
    form = BookForm()
    # Get uniq genres from dodel and set to form
    genre_choices = books.get_unique_genres()
    form.genre.choices = genre_choices

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
        books.save_all()
        flash("Książka została pomyślnie dodana!", "success")
        return redirect(url_for("library"))

    return render_template("library.html", form=form, books=books.all())


@app.route("/library/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)

    form = BookForm(data=book)

    genre_choices = books.get_unique_genres()
    if (book['genre'], book['genre']) not in genre_choices:
        genre_choices.append((book['genre'], book['genre']))
    form.genre.choices = genre_choices

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
    return render_template("book_details.html", form=form, book_id=book_id, book=book)


if __name__ == "__main__":
    app.run(debug=True)

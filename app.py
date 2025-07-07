from flask import Flask, render_template, redirect, url_for, abort
from forms import BookForm
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/library/", methods=["GET", "POST"])
def library():
    form = BookForm()
    if form.validate_on_submit():
        books.create(form.data)
        books.save_all()
        return redirect(url_for("library"))

    return render_template("library.html", form=form, books=books.all())


@app.route("/library/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    try:
        book = books.get(book_id - 1)
    except IndexError:
        abort(404)
    form = BookForm(data=book)

    if form.validate_on_submit():
        books.update(book_id - 1, form.data)
        return redirect(url_for("library"))
    return render_template("book.html", form=form, book_id=book_id, book=book)


if __name__ == "__main__":
    app.run(debug=True)

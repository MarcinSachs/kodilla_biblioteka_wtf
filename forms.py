from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    genre = StringField('Gatunek', validators=[DataRequired()])
    year = IntegerField(
        'Rok',
        validators=[
            DataRequired(message="Pole 'Rok' jest wymagane."),
            NumberRange(min=0, max=datetime.now().year,
                        message="Podaj prawidłowy rok (np. 1999).")
        ])
    submit = SubmitField('Zatwierdź', render_kw={"class": "btn"})

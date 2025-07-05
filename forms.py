from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    genre = StringField('Gatunek', validators=[DataRequired()])
    year = StringField('Rok', validators=[DataRequired()])

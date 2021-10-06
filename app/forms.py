from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


# Файл для html форм
class TestForm(FlaskForm):
    testString = StringField()
    testSubmit = SubmitField()

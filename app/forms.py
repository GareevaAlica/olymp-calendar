from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxForm(FlaskForm):
    choose_olympiads = MultiCheckboxField()
    submit = SubmitField("CHOOSE")

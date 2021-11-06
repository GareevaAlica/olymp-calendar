from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, BooleanField, \
    SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxForm(FlaskForm):
    choose_olympiads = MultiCheckboxField()
    choose_submit = SubmitField("Сохранить изменения")


class SearchForm(FlaskForm):
    olympiad_name_substr = StringField(description="Название олимпиады",
                                       default='')
    choose_fields = MultiCheckboxField(default=[])
    class_range = [str(i) for i in range(1, 12)]
    min_class = SelectField(choices=list(zip(class_range, class_range)),
                            default='1')
    max_class = SelectField(choices=list(zip(class_range, class_range)),
                            default='11')
    user_belong = BooleanField('Мои олимпиады', default=False)
    search_submit = SubmitField("Искать")

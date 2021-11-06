from . import app
from flask import render_template, redirect, session
from app.models import Olympiad, Field, User, SearchParams
from app.forms import MultiCheckboxForm, SearchForm
from app.utils.Google import GoogleCalendar
import google.oauth2.credentials


def indexes_list(class_list):
    indexes = list()
    for my_class in class_list:
        indexes.append(str(my_class.id))
    return indexes


def create_choose_list(all_class_list):
    class_name_list = [c.name for c in all_class_list]
    ids = indexes_list(all_class_list)
    return list(zip(ids, class_name_list))


def get_src(calendar_id):
    return "https://calendar.google.com/calendar/embed?src=" + \
           calendar_id + \
           "&ctz=Europe%2FMoscow"


@app.route("/", methods=['GET'])
def main():
    is_login = True
    if 'credentials' not in session:
        is_login=False
    return render_template("main.html",
                           title='Олимпдейт',
                           is_login=is_login)

@app.route("/choose_olympiads", methods=['GET', 'POST'])
def choose_olympiads():
    is_login = True
    if 'credentials' not in session:
        is_login=False
        return redirect('main')
    choose_form = MultiCheckboxForm()
    search_form = SearchForm()
    user_email = session['user_email']
    calendar_id = User.get_calendar_id(User.get_id(user_email))
    all_olympiads_list = Olympiad.get_all()

    search_form.choose_fields.choices = \
        sorted(create_choose_list(Field.get_all()), key=lambda x: x[1])
    search = SearchParams(search_form.olympiad_name_substr.data,
                          search_form.choose_fields.data,
                          search_form.min_class.data,
                          search_form.max_class.data,
                          user_email if search_form.user_belong.data else None)
    needed_olympiads_id = \
        set([olympiad.id for olympiad in User.search_olympiads(search)])
    if search_form.search_submit.data and search_form.validate_on_submit():
        pass

    choose_form.choose_olympiads.choices = \
        create_choose_list(all_olympiads_list)
    old_olympiads_ids = User.get_olympiads_id_by_user_email(user_email)
    if choose_form.choose_submit.data and choose_form.validate_on_submit():
        new_olympiads_ids = list(map(int, choose_form.choose_olympiads.data))
        old_olympiads_ids = list(set(old_olympiads_ids) - \
                                 (set(old_olympiads_ids) - set(
                                     needed_olympiads_id)))
        credentials = \
            google.oauth2.credentials.Credentials(**session['credentials'])
        try:
            google_calendar = GoogleCalendar(calendar_id, credentials)
            google_calendar.update_olympiad_events(all_olympiads_list,
                                                   old_olympiads_ids,
                                                   new_olympiads_ids)
        except:
            return redirect('main')
        User.save_olympiad_list(user_email, new_olympiads_ids)
        choose_form.choose_olympiads.data = list(map(str, new_olympiads_ids))
    else:
        choose_form.choose_olympiads.data = list(map(str, old_olympiads_ids))
    return render_template("choose_olympiads.html",
                           choose_form=choose_form,
                           search_form=search_form,
                           needed_olympiads_id=needed_olympiads_id,
                           src=get_src(calendar_id),
                           title='Поиск',
                           is_login=is_login)


# Если страницы не существует - перенаправляем на главную.
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route("/myolymps", methods=['GET'])
def myolymps():
    is_login = True
    if 'credentials' not in session:
        is_login=False
    user_email = session['user_email']
    olympiads_list = User.get_olympiads_by_user_email(user_email)
    return render_template("myolymps.html",
                           olympiads_list=olympiads_list,
                           title='Мой список',
                           is_login=is_login)
                           
@app.route("/about", methods=['GET'])
def about():
    is_login = True
    if 'credentials' not in session:
        is_login=False
    return render_template("about.html",
                           title='О проекте',
                           is_login=is_login)
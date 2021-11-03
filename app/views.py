from . import app
from flask import render_template, redirect, session
from app.models import Olympiad, User
from app.forms import MultiCheckboxForm
from app.utils.Google import GoogleCalendar
import google.oauth2.credentials


def indexes_list(olympiads_list):
    indexes = list()
    for olympiad in olympiads_list:
        indexes.append(str(olympiad.id))
    return indexes


def get_src(calendar_id):
    return "https://calendar.google.com/calendar/embed?src=" + \
           calendar_id + \
           "&ctz=Europe%2FMoscow"


@app.route("/", methods=['GET'])
def main():
    return render_template("main.html",
                           title='Главная')


@app.route("/choose_olympiads", methods=['GET', 'POST'])
def choose_olympiads():
    if 'credentials' not in session:
        return redirect('main')
    form = MultiCheckboxForm()
    user_email = session['user_email']
    calendar_id = User.get_calendar_id(User.get_id(user_email))

    all_olympiads_list = Olympiad.get_all()
    olympiads_name_list = [olympiad.name for olympiad in all_olympiads_list]
    ids = list(map(str, range(1, len(all_olympiads_list) + 1)))
    form.choose_olympiads.choices = list(zip(ids, olympiads_name_list))

    old_olympiads_ids = User.get_olympiads_id_by_user_email(user_email)
    if form.validate_on_submit():
        new_olympiads_ids = list(map(int, form.choose_olympiads.data))
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
        return redirect('/choose_olympiads')
    form.choose_olympiads.data = list(map(str, old_olympiads_ids))
    return render_template("choose_olympiads.html",
                           form=form,
                           olympiads_list=all_olympiads_list,
                           src=get_src(calendar_id),
                           title='Выбор олимпиад')


# Если страницы не существует - перенаправляем на главную.
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

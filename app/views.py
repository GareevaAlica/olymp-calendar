from . import app
from flask import render_template, redirect, session
from app.models import Olympiad, User
from app.forms import MultiCheckboxForm
from app.utils.Google import GoogleCalendar
from datetime import date
from typing import NamedTuple
import google.oauth2.credentials


class OlympiadInfoTuple(NamedTuple):
    olympiad_name: str
    olympiad_url: str
    events: list
    classes: str
    fields: list


class EventTuple(NamedTuple):
    event_name: str
    date_start: date
    date_end: date


def get_olympiads_info_list(olympiads_list, indexes):
    olympiads_info_list = list()
    for id in indexes:
        olympiad = olympiads_list[int(id)]
        events_list = list()
        for event in olympiad.events:
            events_list.append(EventTuple(event.name,
                                          event.date_start,
                                          event.date_end))
        olympiads_info_list.append(
            OlympiadInfoTuple(olympiad.name,
                              olympiad.url,
                              events_list,
                              olympiad.classes,
                              list()))
    return olympiads_info_list


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
    # список всех олимпиад
    olympiads_list = Olympiad.get_all()
    calendar_id = \
        User.get_calendar_id(User.get_id(session['credentials']['client_id']))

    olympiads_name_list = [olympiad.name for olympiad in olympiads_list]
    ids = list(map(str, range(len(olympiads_list))))
    form.choose_olympiads.choices = list(zip(ids, olympiads_name_list))

    if form.validate_on_submit():
        indexes = form.choose_olympiads.data
        olympiads_info_list = get_olympiads_info_list(olympiads_list, indexes)
        credentials = \
            google.oauth2.credentials.Credentials(**session['credentials'])
        google_calendar = GoogleCalendar(calendar_id, credentials)
        google_calendar.create_olympiad_events(olympiads_info_list)
        return redirect('/choose_olympiads')
    return render_template("choose_olympiads.html",
                           form=form,
                           olympiads_list=olympiads_list,
                           src=get_src(calendar_id),
                           title='Выбор олимпиад')


# Если страницы не существует - перенаправляем на главную.
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

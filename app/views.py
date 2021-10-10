from . import app
from flask import render_template, redirect
from app.models import Olympiad, Event


# Главная страница.
@app.route("/", methods=['GET', 'POST'])
def main():
    olympiads_list = Olympiad.get_all()
    return render_template("main.html",
                           olympiads_list=olympiads_list,
                           title='Главная')


# Если страницы не существует - перенаправляем на главную.
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

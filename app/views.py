from . import app
from flask import render_template, redirect


# Главная страница.
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("main.html",
                           title='Главная')


# Если страницы не существует - перенаправляем на главную.
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)  # создаем приложение на Flask
app.config.from_object('config')  # загрузка настроек из config.py

# Создаем базу данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import views, models
from .utils import Auth

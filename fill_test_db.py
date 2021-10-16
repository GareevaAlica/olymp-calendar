from app.models import Olympiad, Event
from app import db
from app.utils.DatabaseUpdater import DatabaseUpdater
from datetime import date


# Файл заполнения базы данных для тестов

def create_olympiad(name, url=None):
    olympiad = Olympiad(name=name, url=url)
    olympiad.save()
    print(olympiad)


def create_event(olympiad_id, name, date_start=None, date_end=None):
    event = Event(olympiad_id=olympiad_id, name=name,
                  date_start=date_start, date_end=date_end)
    event.save()
    print(event)


db.drop_all()  # удалить старые данные
db.create_all()  # создать базу

# вызов заполнения базы данных
db_updater = DatabaseUpdater()
# db_updater.update_database() долгий парсинг информации
# получение уже собранной информации из /test_db/olympiads_info_list.json
db_updater.save_olympiads_info_from_json()

db.session.commit()  # обновляем базу
print('Success')

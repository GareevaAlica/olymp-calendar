from app.models import Olympiad, Event, User
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


def create_user(client_id, calendar_id):
    user = User(client_id=client_id, calendar_id=calendar_id)
    user.save()
    print(user)


db.drop_all()  # удалить старые данные
db.create_all()  # создать базу

# вызов заполнения базы данных
db_updater = DatabaseUpdater()
# долгий парсинг информации
# db_updater.update_database(True)
# получение уже собранной информации из /test_db/olympiads_info_list.json
db_updater.save_olympiads_info_from_json()

client_id = '529021305325-8vvgsbl0j5sh6r9gqdg3bvaflabc2cge.apps.googleusercontent.com'
create_user(client_id,
            'u54rqm90ph7enrmdu7tk2ol4l8@group.calendar.google.com')

User.save_olympiad_list(client_id, [i for i in range(30)])

db.session.commit()  # обновляем базу
print('Success')

from app.models import Olympiad, Event, User
from app import db
from app.utils.DatabaseUpdater import DatabaseUpdater

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


def create_user(user_email, calendar_id):
    user = User(user_email=user_email, calendar_id=calendar_id)
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

user_email = 'alica.gareeva@gmail.com'
create_user(user_email,
            'u54rqm90ph7enrmdu7tk2ol4l8@group.calendar.google.com')

User.save_olympiad_list(user_email, [i for i in range(30)])

db.session.commit()  # обновляем базу
print('Success')

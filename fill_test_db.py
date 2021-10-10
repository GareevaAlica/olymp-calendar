from app.models import Olympiad, Event
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


db.drop_all()  # удалить старые данные
db.create_all()  # создать базу


# пару тестовых данных
create_olympiad(name="olympiad1", url="url1")
create_event(olympiad_id=1, name='event1',
             date_start='date_start1', date_end='date_end1')
create_event(olympiad_id=1, name='event2',
             date_start='date_start2', date_end='date_end2')

create_olympiad(name="olympiad2", url="url1")
create_event(olympiad_id=2, name='event3',
             date_start='date_start3', date_end='date_end3')

# вызов заполнения базы данных реальной информацией
db_updater = DatabaseUpdater()
db_updater.update_database()

db.session.commit()  # обновляем базу
print('Success')

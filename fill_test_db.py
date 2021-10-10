from app.models import Olympiad, Event
from app import db

# Файл заполнения базы данных для тестов

db.drop_all()  # удалить старые данные
db.create_all()  # создать базу

olympiad1 = Olympiad(name="olympiad1", link="link1")
Olympiad.save(olympiad1)
print(olympiad1)

event1 = Event(olympiad_id=1, name='event1',
               data_start='data_start1', data_end='data_end1')
Event.save(event1)
print(event1)

event2 = Event(olympiad_id=1, name='event2',
               data_start='data_start2', data_end='data_end2')
Event.save(event2)
print(event2)

# ------------------------------------
olympiad2 = Olympiad(name="olympiad2", link="link2")
Olympiad.save(olympiad2)
print(olympiad2)

event3 = Event(olympiad_id=2, name='event3',
               data_start='data_start3', data_end='data_end3')
Event.save(event3)
print(event3)

db.session.commit()  # обновляем базу
print('Success')

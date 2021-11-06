from app.models import User
from app import db
from app.utils.DatabaseUpdater import DatabaseUpdater


db.drop_all()  # удалить старые данные
db.create_all()  # создать базу

# вызов заполнения базы данных
db_updater = DatabaseUpdater()

# долгий парсинг информации
# db_updater.update_database(True)

# получение уже собранной информации из /test_db/olympiads_info_list.json
db_updater.save_olympiads_info_from_json()

db.session.commit()  # обновляем базу
print('Success')

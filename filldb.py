from app.models import User
from app import db

# Файл заполнения базы данных для тестов

db.drop_all()  # удалить старые данные
db.create_all()  # создать базу

# Создаем юзера с никнеймом FirstUser
user = User(username="FirstUser")
User.save(user)  # сохраняем его

db.session.commit()  # обновляем базу
print('Success')

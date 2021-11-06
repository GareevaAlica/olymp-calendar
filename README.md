> Командный проект для проектного семинара.
> * [Гареева Алиса] - project manager, backend developer (работа с созданием flask приложения)
> * [Бордюгов Максим], [Ичалов Леонид], [Леванков Егор] - backend developers (работа с остальными технологиями: парсингом(BeautifulSoup), API и OAuth)
> * [Шатская Лиза]  - frontend developer, формулировка конечного результата
>  
> октябрь 2021
___

# Олимпиадный календарь

## О проекте

[Спецификация требований программного обеспечения]

Web-сервис для помощи планирования участия в олимпиадах на 2021/22 учебный год, используя [Google Calendar] с удобным поиском интересующих олимпиад по различным фильтрам и просмотром назначенного плана.

Сайт позволяет пользователям авторизоваться через гугл-аккаунт, предоставив доступ для изменения гугл-календаря и получения информации об аккаунте. После пользователь выбирает интересующие его школьные олимпиады из перечня с помощью фильтров, и сервис автоматически заносит даты их проведения со ссылками на их официальные источники в новый созданный гугл-календарь. Сервис запоминает старые настройки и позволяет при следующем использовании, изменять уже существующий список олимпиад пользователя, причем не создавая новый календарь.

## Настройка OAuth 2.0
[OAuth 2.0] используется для авторизации в google аккаунте, чтобы приложение могло в сервисе [Google Calendar] создавать календари и создавать\удалять события у конкретного пользователя.

1. Переходим в [OAuth consent screen] из APIs & Services и настраиваем приложение:
  * заполняем нужные данные
  * в *Scopes* добавляем *https://www.googleapis.com/auth/userinfo.email* (доступ к информации об аккаунте) и *https://www.googleapis.com/auth/calendar* (доступ к [Google Calendar] для изменения)
  * в *Test users* добавляем пользователей, которые смогут пользоваться авторизацией в приложении

2. Переходим в [Credentials] из APIs & Services и создаем Client ID:
  * *CREATE CREDENTIALS* -> *OAuth client ID*
  * *Application type* -> *Web application*
  * заполняем нужные данные
  * в *Authorized redirect URIs* добавляем URI *http://localhost:5000/oauth_callback*

3. Переходим на страницу *Client ID for Web application* из [Credentials] и сохраняем данные в формате *.json* (*DOWNLOAD JSON*)

## Запуск приложения

1. Создание виртуального окружения:
```
conda create -n py38_webapp_env python=3.8
conda activate py38_webapp_env
```

2. Установка нужных библиотек:
```
pip install -r requirements.txt
```

3. Настройка файла */config.py*:
* добавление информации для OAuth 2.0:
  * *CLIENT_SECRET* - путь к *.json* файлу, где лежат данные для доступа к [OAuth 2.0]

4. Настройка базы данных:

Создание
```
export FLASK_APP=main.py (или set FLASK_APP=main.py , если не выходит первое)
flask db init
flask db migrate
flask db upgrade
```

Заполнение
```
python fill_db.py
```

5. Запуск приложения:

```
python main.py
```
Итого, приложение было запущено на http://localhost:5000/

## Использованные технологии

* [OAuth 2.0] - используется для авторизации в google аккаунте
* [Google Calendar API] - позволяет создавать календари и создавать\удалять события в них
* Python+BeautifulSoup+Flask+SQLAlchemy+Bootstap


[Гареева Алиса]:<https://github.com/GareevaAlice>
[Бордюгов Максим]:<https://github.com/DedAzaMarks>
[Ичалов Леонид]:<https://github.com/Leo-nid>
[Леванков Егор]:<https://github.com/elevankoff>
[Шатская Лиза]:<https://github.com/NanamyYu>
[Спецификация требований программного обеспечения]:<https://docs.google.com/document/d/1XFEL_6hiaVhY-LgMXNDbAMNh4pqtLTjGomNfn3OpKzw/edit?usp=sharing>
[OAuth 2.0]:<https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps>
[OAuth consent screen]:<https://console.cloud.google.com/apis/credentials/consent>
[Credentials]:<https://console.cloud.google.com/apis/credentials>
[Google Calendar]:<https://calendar.google.com/calendar>
[Google Calendar API]:<https://developers.google.com/calendar/api>

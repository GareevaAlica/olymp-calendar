from app import db
from app.utils.Google import GoogleCalendar
import google.oauth2.credentials

class Olympiad(db.Model):
    # id олимпиады в базе данных
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # название олимпиады
    name = db.Column(db.String)
    # ссылка олимпиады на https://olimpiada.ru
    url = db.Column(db.String)
    # классы
    classes = db.Column(db.String)
    # события проведения олимпиады
    events = db.relationship('Event', backref='olympiad', lazy='dynamic')

    def __init__(self, name, url=None, classes=None):
        self.name = name
        self.url = url
        self.classes = classes

    def __repr__(self):
        return '<Olympiad: name = {},' \
               ' url = {},' \
               ' classes = {}>'.format(self.name, self.url, self.classes)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Olympiad.query.all()


class Event(db.Model):
    # id события в базе данных
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id олимпиады в базе данных, которой принадлежит событие
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.id'))
    # название события
    name = db.Column(db.String, nullable=False)
    # дата начала проведения события
    date_start = db.Column(db.Date)
    # дата конца проведения события
    date_end = db.Column(db.Date)

    def __repr__(self):
        return '<Event: olympiad_id = {}, name = {},' \
               ' date_start = {}, date_end = {}>'.format(self.olympiad_id,
                                                         self.name,
                                                         self.date_start,
                                                         self.date_end)

    def __init__(self, olympiad_id, name, date_start=None, date_end=None):
        self.olympiad_id = olympiad_id
        self.name = name
        self.date_start = date_start
        self.date_end = date_end

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String, unique=True,)
    calendar_id = db.Column(db.String, unique=True)

    def __repr__(self):
        return '<User: client_id = {}, calendar_id = {}'.format(self.client_id,
                                                            self.calendar_id)

    def __init__(self, client_id, calendar_id):
        self.client_id = client_id
        self.calendar_id = calendar_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_client_id(id):
        client_id = User.query.filter_by(id=id).first().client_id
        return client_id

    @staticmethod
    def get_calendar_id(id):
        calendar_id = User.query.filter_by(id=id).first().calendar_id
        return calendar_id

    @staticmethod
    def get_id(client_id):
        id = User.query.filter_by(client_id=client_id).first().id
        return id

    @staticmethod
    def client_id_exists(client_id):
        if User.query.filter_by(client_id=client_id).first() is None:
            return False
        return True

    @staticmethod
    def try_add_user(client_id, credentials):
        if not User.client_id_exists(client_id):
            google_calendar = GoogleCalendar(credentials)
            calendar_id = google_calendar.create_calendar()
            user = User(client_id=client_id, calendar_id=calendar_id)
            user.save()
            print(user)

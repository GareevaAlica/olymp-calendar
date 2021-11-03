from app import db
from app.utils.Google import GoogleCalendar
from sqlalchemy import delete

olympiads_fields = \
    db.Table('olympiads_fields', db.Model.metadata,
             db.Column('olympiad_id', db.Integer, db.ForeignKey('olympiad.id')),
             db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
             )

users_olympiads = \
    db.Table('users_olympiads', db.Model.metadata,
             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
             db.Column('olympiad_id', db.Integer, db.ForeignKey('olympiad.id'))
             )


class Olympiad(db.Model):
    __tablename__ = 'olympiad'
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
    fields = db.relationship('Field', secondary=olympiads_fields)

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

    @staticmethod
    def get_by_id(id):
        return Olympiad.query.filter_by(id=id).first()

    @staticmethod
    def save_field(olympiad_id, field_id):
        olympiad = Olympiad.get_by_id(olympiad_id)
        field = Field.get_by_id(field_id)
        olympiad.fields.append(field)
        olympiad.save()

    @staticmethod
    def save_field_list(olympiad_id, field_name_list):
        for field_name in field_name_list:
            field_id = Field.get_or_create(field_name)
            Olympiad.save_field(olympiad_id, field_id)


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


class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Field: name = {}>'.format(self.name)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_by_id(id):
        return Field.query.filter_by(id=id).first()

    @staticmethod
    def get_or_create(name):
        search_field = Field.query.filter_by(name=name).first()
        if search_field is None:
            field = Field(name=name)
            return field.save()
        else:
            return search_field.id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, unique=True)
    calendar_id = db.Column(db.String, unique=True)
    olympiads = db.relationship('Olympiad', secondary=users_olympiads)

    def __repr__(self):
        return '<User: user_email = {}, calendar_id = {}>'.format(
            self.user_email,
            self.calendar_id)

    def __init__(self, user_email, calendar_id):
        self.user_email = user_email
        self.calendar_id = calendar_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_user_email(user_email):
        return User.query.filter_by(user_email=user_email).first()

    @staticmethod
    def get_user_email(id):
        user_email = User.query.filter_by(id=id).first().user_email
        return user_email

    @staticmethod
    def get_calendar_id(id):
        calendar_id = User.query.filter_by(id=id).first().calendar_id
        return calendar_id

    @staticmethod
    def get_id(user_email):
        id = User.query.filter_by(user_email=user_email).first().id
        return id

    @staticmethod
    def get_olympiads_by_user_email(user_email):
        return User.query.filter_by(user_email=user_email).first().olympiads

    @staticmethod
    def get_olympiads_id_by_user_email(user_email):
        olympiads = \
            User.query.filter_by(user_email=user_email).first().olympiads
        olympiads_id = list()
        for olympiad in olympiads:
            olympiads_id.append(olympiad.id)
        return olympiads_id

    @staticmethod
    def user_email_exists(user_email):
        if User.query.filter_by(user_email=user_email).first() is None:
            return False
        return True

    @staticmethod
    def try_add_user(user_email, credentials):
        if not User.user_email_exists(user_email):
            google_calendar = GoogleCalendar(None, credentials)
            calendar_id = google_calendar.create_calendar()
            user = User(user_email=user_email, calendar_id=calendar_id)
            user.save()
            print(user)

    @staticmethod
    def save_olympiad(user_email, olympiad_id):
        olympiad = Olympiad.get_by_id(olympiad_id)
        user = User.get_by_user_email(user_email)
        user.olympiads.append(olympiad)
        user.save()

    @staticmethod
    def save_olympiad_list(user_email, olympiad_id_list):
        User.delete_olympiads(user_email)
        for olympiad_id in olympiad_id_list:
            User.save_olympiad(user_email, int(olympiad_id))

    @staticmethod
    def delete_olympiads(user_email):
        user_id = User.get_id(user_email)
        deleted_users_olympiads = \
            delete(users_olympiads).where(users_olympiads.c.user_id == user_id)
        db.session.execute(deleted_users_olympiads)
        db.session.commit()

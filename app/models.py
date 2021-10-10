from app import db


class Olympiad(db.Model):
    # id олимпиады в базе данных
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # название олимпиады
    name = db.Column(db.String, unique=True, nullable=False)
    # ссылка олимпиады на https://olimpiada.ru
    url = db.Column(db.String)
    # события проведения олимпиады
    events = db.relationship('Event', backref='olympiad', lazy='dynamic')

    def __init__(self, name, url=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Olympiad: name = {}, url = {}>'.format(self.name, self.url)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Olympiad.query.all()

    @staticmethod
    def get_id_by_url(url):
        id = Olympiad.query.filter_by(url=url).first().id
        return id

    @staticmethod
    def get_name(id):
        name = Olympiad.query.filter_by(id=id).first().name
        return name

    @staticmethod
    def get_url(id):
        url = Olympiad.query.filter_by(id=id).first().url
        return url

    @staticmethod
    def get_events(id):
        events = Olympiad.query.filter_by(id=id).first().events
        return events


class Event(db.Model):
    # id события в базе данных
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id олимпиады в базе данных, которой принадлежит событие
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.id'))
    # название события
    name = db.Column(db.String, nullable=False)
    # дата начала проведения события
    date_start = db.Column(db.String)
    # дата конца проведения события
    date_end = db.Column(db.String)

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

    @staticmethod
    def get_olympiad_id(id):
        olympiad_id = Event.query.filter_by(id=id).first().olympiad_id
        return olympiad_id

    @staticmethod
    def get_name(id):
        name = Event.query.filter_by(id=id).first().name
        return name

    @staticmethod
    def get_date_start(id):
        date_start = Event.query.filter_by(id=id).first().date_start
        return date_start

    @staticmethod
    def get_date_end(id):
        date_end = Event.query.filter_by(id=id).first().date_end
        return date_end

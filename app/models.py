from app import db


class Olympiad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    link = db.Column(db.String)
    events = db.relationship('Event', backref='olympiad', lazy='dynamic')

    def __init__(self, name, link=None):
        self.name = name
        self.link = link

    def __repr__(self):
        return '<Olympiad: name = {}, link = {}>'.format(self.name, self.link)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_name(id):
        name = Olympiad.query.filter_by(id=id).first().name
        return name

    @staticmethod
    def get_link(id):
        link = Olympiad.query.filter_by(id=id).first().link
        return link

    @staticmethod
    def get_events(id):
        events = Olympiad.query.filter_by(id=id).first().events
        return events


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.id'))
    name = db.Column(db.String, nullable=False)
    data_start = db.Column(db.String)
    data_end = db.Column(db.String)

    def __repr__(self):
        return '<Event: olympiad_id = {}, name = {},' \
               ' data_start = {}, data_end = {}>'.format(self.olympiad_id,
                                                         self.name,
                                                         self.data_start,
                                                         self.data_end)

    def __init__(self, olympiad_id, name, data_start=None, data_end=None):
        self.olympiad_id = olympiad_id
        self.name = name
        self.data_start = data_start
        self.data_end = data_end

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
    def get_data_start(id):
        data_start = Event.query.filter_by(id=id).first().data_start
        return data_start

    @staticmethod
    def get_data_end(id):
        data_end = Event.query.filter_by(id=id).first().data_end
        return data_end

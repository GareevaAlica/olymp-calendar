from app import db

# Файл для классов базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

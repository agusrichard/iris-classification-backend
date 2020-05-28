from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(80))
    irises = db.relationship('Iris', backref='user', lazy=True)

    def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Iris(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petal_length = db.Column(db.Float)
    petal_width = db.Column(db.Float)
    sepal_length = db.Column(db.Float)
    sepal_width = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Iris('{self.id}', '{self.user_id}')"

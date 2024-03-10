from utils import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    cart = db.relationship('Cart', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def toDict(self):
        return {
            "username": self.username,
            "email": self.email,
            "passworrd": self.password,
        }

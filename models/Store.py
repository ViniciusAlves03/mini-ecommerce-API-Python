from utils.db import db

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cnpj = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Store %r>' % self.username

    def toDict(self):
        return {
            "username": self.username,
            "email": self.email,
            "cnpj": self.cnpj,
            "passworrd": self.password,
        }

from utils.db import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

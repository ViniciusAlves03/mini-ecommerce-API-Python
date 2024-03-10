from utils import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, cart_id, product_id, quantity=1):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

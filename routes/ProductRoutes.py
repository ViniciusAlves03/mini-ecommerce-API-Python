from flask import Blueprint, jsonify, request
from utils.db import db
from models.Store import Store
from models.Product import Product

productBp = Blueprint('product', __name__)

@productBp.route('/products', methods=['GET'])
def getProducts():
    products = Product.query.all()
    return jsonify([product.toDict() for product in products])

@productBp.route('/store/<int:store_id>/products', methods=['POST'])
def createProduct(store_id):
    data = request.get_json()
    store = Store.query.get_or_404(store_id)
    product = Product(**data, store=store)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.toDict()), 201

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['GET'])
def getProduct(store_id, product_id):
    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    return jsonify(product.toDict())

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['PUT'])
def updateProduct(store_id, product_id):
    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    data = request.get_json()

    allowed_keys = ['name', 'price']
    for key, value in data.items():
        if key in allowed_keys:
            setattr(product, key, value)

    db.session.commit()
    return jsonify(product.toDict())

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['DELETE'])
def deleteProduct(store_id, product_id):
    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

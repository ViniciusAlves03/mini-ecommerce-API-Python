from flask import Blueprint, jsonify, request
from utils import db
from models import Store, Product
from auth_jwt import token_verify

productBp = Blueprint('product', __name__)

@productBp.route('/products', methods=['GET'])
def getProducts():
    products = Product.query.all()
    return jsonify([product.toDict() for product in products])

@productBp.route('/store/<int:store_id>/products', methods=['POST'])
@token_verify
def createProduct(token_uid, store_id):

    if token_uid != store_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    data = request.get_json()
    store = Store.query.get_or_404(store_id)
    product = Product(**data, store=store)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.toDict()), 201

@productBp.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    product = Product.query.filter_by(name=product_name).first_or_404()
    return jsonify(product.toDict())

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['GET'])
def getProductInStore(store_id, product_id):
    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    return jsonify(product.toDict())

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['PUT'])
@token_verify
def updateProduct(token_uid, store_id, product_id):

    if token_uid != store_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    data = request.get_json()

    allowed_keys = ['name', 'price', 'quantity']
    for key, value in data.items():
        if key in allowed_keys:
            setattr(product, key, value)

    db.session.commit()
    return jsonify(product.toDict())

@productBp.route('/store/<int:store_id>/products/<int:product_id>', methods=['DELETE'])
@token_verify
def deleteProduct(token_uid, store_id, product_id):

    if token_uid != store_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    product = Product.query.filter_by(id=product_id, store_id=store_id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

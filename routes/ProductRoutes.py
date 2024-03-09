from flask import Blueprint, jsonify, request
from utils.db import db
from models.Product import Product

productBp = Blueprint('product', __name__)

@productBp.route('/products', methods=['GET'])
def getProducts():
    """
    Allows users to view all products (public access).
    """
    products = Product.query.all()
    return jsonify([product.toDict() for product in products])

@productBp.route('/product/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    """
    Allows users to view a specific product (public access).
    """
    product = Product.query.get_or_404(product_id)
    return jsonify(product.toDict())

@productBp.route('/product', methods=['POST'])
#@token_required  # Require token for store role
def createProduct():
    """
    Allows stores to create new products (requires store token).
    """
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.toDict()), 201

@productBp.route('/product/<int:product_id>', methods=['PUT'])
#@token_required  # Require token for store role
def updateProduct(product_id):
    """
    Allows stores to update their products (requires store token).
    """
    store = Product.query.get_or_404(product_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(store, key, value)
    db.session.commit()
    return jsonify(store.toDict())

@productBp.route('/product/<int:product_id>', methods=['DELETE'])
#@token_required  # Require token for store role
def deleteProduct(product_id):
    """
    Allows stores to delete their products (requires store token).
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

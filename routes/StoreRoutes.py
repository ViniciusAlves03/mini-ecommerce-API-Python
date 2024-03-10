from flask import Blueprint, jsonify, request
from utils.db import db
from models.Store import Store

storeBp = Blueprint('store', __name__)

@storeBp.route('/stores', methods=['GET'])
def getStores():
    stores = Store.query.all()
    return jsonify([store.toDict() for store in stores])

@storeBp.route('/store', methods=['POST'])
def createStore():
    data = request.get_json()
    store = Store(**data)
    db.session.add(store)
    db.session.commit()
    return jsonify(store.toDict()), 201

@storeBp.route('/store/<int:store_id>', methods=['GET'])
def getStore(store_id):
    store = Store.query.get_or_404(store_id)
    return jsonify([store.toDict()])

@storeBp.route('/store/<int:store_id>', methods=['PUT'])
def updateStore(store_id):
    store = Store.query.get_or_404(store_id)
    data = request.get_json()

    allowed_keys = ['username', 'email', 'cnpj']
    for key, value in data.items():
        if key in allowed_keys:
            setattr(store, key, value)

    db.session.commit()
    return jsonify(store.toDict())

@storeBp.route('/store/<int:store_id>', methods=['DELETE'])
def deleteStore(store_id):
    store = Store.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

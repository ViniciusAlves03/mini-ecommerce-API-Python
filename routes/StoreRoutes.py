from flask import Blueprint, jsonify, request
from utils import db
from models import Store
from auth_jwt import token_creator, token_verify

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

@storeBp.route('/store/login', methods=['POST'])
def loginUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if (not (username and password)):
        return jsonify({'message': 'Nome de usuário ou senha ausente!'}), 401

    store = Store.query.filter_by(username=username, password=password).first_or_404()

    token = token_creator.create(store.id)
    return jsonify({'token': token}), 200

@storeBp.route('/store/<int:store_id>', methods=['GET'])
def getStore(store_id):
    store = Store.query.get_or_404(store_id)
    return jsonify([store.toDict()])

@storeBp.route('/store/<int:store_id>', methods=['PUT'])
@token_verify
def updateStore(token_uid, store_id):

    if token_uid != store_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    store = Store.query.get_or_404(store_id)
    data = request.get_json()

    allowed_keys = ['username', 'email', 'cnpj', 'password']
    for key, value in data.items():
        if key in allowed_keys:
            setattr(store, key, value)

    db.session.commit()
    return jsonify(store.toDict())

@storeBp.route('/store/<int:store_id>', methods=['DELETE'])
@token_verify
def deleteStore(token_uid, store_id):

    if token_uid != store_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    store = Store.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

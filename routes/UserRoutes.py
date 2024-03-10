from flask import Blueprint, jsonify, request
from utils import db
from models import User
from auth_jwt import token_creator, token_verify

userBp = Blueprint('user', __name__)

@userBp.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    return jsonify([user.toDict() for user in users])

@userBp.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.toDict()), 201

@userBp.route('/user/login', methods=['POST'])
def loginUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if (not (username and password)):
        return jsonify({'message': 'Nome de usuário ou senha ausente!'}), 401

    user = User.query.filter_by(username=username, password=password).first_or_404()

    token = token_creator.create(user.id)
    return jsonify({'token': token}), 200

@userBp.route('/user/<int:user_id>', methods=['GET'])
@token_verify
def getUser(token_uid, user_id):

    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    #return jsonify([user.toDict()])
    return jsonify({
        'username': user.username,
        "email": user.email
    })

@userBp.route('/user/<int:user_id>', methods=['PUT'])
@token_verify
def updateUser(token_uid, user_id):

    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    allowed_keys = ['username', 'email', 'password']
    for key, value in data.items():
        if key in allowed_keys:
            setattr(user, key, value)

    db.session.commit()
    return jsonify(user.toDict())

@userBp.route('/user/<int:user_id>', methods=['DELETE'])
@token_verify
def deleteUser(token_uid, user_id):

    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

from flask import Blueprint, jsonify, request
from utils.db import db
from models.User import User

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

@userBp.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([user.toDict()])

@userBp.route('/user/<int:user_id>', methods=['PUT'])
def updateUser(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.toDict())

@userBp.route('/user/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso!"}), 200

from functools import wraps
from flask import jsonify, request
import jwt
from config import jwt_config
from .token_handler import token_creator

def token_verify(function: callable) -> callable:

    @wraps(function)
    def decorated(*args, **kwargs):
        raw_token = request.headers.get("Authorization")

        if not raw_token:
            return jsonify({
                'error': 'Não autorizado!'
            }), 400

        try:
            token = raw_token.split()[1]
            token_information = jwt.decode(token, key=jwt_config["TOKEN_KEY"], algorithms="HS256")
            token_uid = token_information["uid"]
        except jwt.InvalidSignatureError:
            return jsonify({
                'error': 'Token inválido!'
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token expirado!'
            }), 401
        except KeyError as e:
            return jsonify({
                'error': 'Token inválido2'
            }), 401

        next_token = token_creator.refresh(token)
        return function(token_uid, *args, **kwargs)

    return decorated

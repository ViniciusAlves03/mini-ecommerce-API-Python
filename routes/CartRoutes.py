from flask import Blueprint, jsonify, request
from auth_jwt import token_verify
from utils import db
from models import User, Product, Cart

cartBp = Blueprint('cart', __name__)

@cartBp.route('/user/<int:user_id>/cart', methods=['GET'])
@token_verify
def getCart(token_uid, user_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    cart_items = user.cart

    cart_data = [{'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]

    return jsonify(cart_data)


@cartBp.route('/user/<int:user_id>/cart/add', methods=['POST'])
@token_verify
def addToCart(token_uid, user_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    data = request.get_json()
    product_id = data.get('id')
    quantity = 1

    if data.get('quantity'):
        quantity = data.get('quantity')

    if not product_id:
        return jsonify({'message': 'Informe o ID do produto!'}), 400

    product = Product.query.get_or_404(product_id)

    user = User.query.get_or_404(user_id)
    cart_item = Cart.query.filter_by(cart_id=user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        new_item = Cart(user.id, product_id, quantity)
        db.session.add(new_item)

    db.session.commit()
    return jsonify({'message': 'Item adicionado ao carrinho!'}), 200


@cartBp.route('/user/<int:user_id>/cart/update/<int:product_id>', methods=['PUT'])
@token_verify
def updateCartItem(token_uid, user_id, product_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    data = request.get_json()
    quantity = data.get('quantity')

    if not quantity:
        return jsonify({'message': 'Informe a quantidade!'}), 400

    user = User.query.get_or_404(user_id)
    cart_item = Cart.query.filter_by(cart_id=user.id, product_id=product_id).first_or_404()

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({'message': 'Quantidade atualizada!'}), 20

@cartBp.route('/user/<int:user_id>/cart/buy_all', methods=['POST'])
@token_verify
def buyAll(token_uid, user_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    cart_items = Cart.query.filter_by(cart_id=user.id).all()

    for item in cart_items:
        product = Product.query.filter_by(id=item.product_id).first_or_404()

        if product.quantity - item.quantity < 0:
            return jsonify({'message': 'Não será efetuada a compra, quantidade maior do que a disponível!'}), 200
        else:
            product.quantity -= item.quantity
            db.session.delete(item)
            db.session.commit()

    return jsonify({'message': 'Todos os produtos comprados!'}), 200


@cartBp.route('/user/<int:user_id>/cart/buy_item/<int:product_id>', methods=['POST'])
@token_verify
def buyItem(token_uid, user_id, product_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    cart_item = Cart.query.filter_by(cart_id=user.id, product_id=product_id).first_or_404()
    product = Product.query.filter_by(id=cart_item.product_id).first_or_404()
    product.quantity -= cart_item.quantity

    if product.quantity - cart_item.quantity < 0:
        return jsonify({'message': 'Não será efetuada a compra, quantidade maior do que a disponível!'}), 200
    else:
        product.quantity -= cart_item.quantity
        db.session.delete(cart_item)
        db.session.commit()

    return jsonify({'message': 'Produto comprado!'}), 200


@cartBp.route('/user/<int:user_id>/cart/delete_item/<int:product_id>', methods=['DELETE'])
@token_verify
def deleteItem(token_uid, user_id, product_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    cart_item = Cart.query.filter_by(cart_id=user.id, product_id=product_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Produto removido do carrinho!'}), 200


@cartBp.route('/user/<int:user_id>/cart/clear', methods=['DELETE'])
@token_verify
def clearCart(token_uid, user_id):
    if token_uid != user_id:
        return jsonify({'message': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    Cart.query.filter_by(cart_id=user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Carrinho esvaziado!'}), 200


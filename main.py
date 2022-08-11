# Create Evgeniy Tabashnyuk
# 10.08.2022

from datetime import datetime
from flask import (
    Flask,
    abort,
    jsonify,
    json,
    request,
)

from app import (
    app,
    db,
    auth,
)
from config import Config
from generation import Generator
from models.models import Card, Status, Transaction, User
from models.schemas import (
    CardSchema,
    TransactionSchema,
    UserSchema,
    UserRegisterSchema,
)
import time
import utils


@auth.verify_password
def verify(email: str, password: str):
    if not (email and password):
        return False
    user: User = User.get_by_email(email)
    return user.verify_password(password)


@app.route("/api/user", methods=["GET"])
@auth.login_required
def get_user_list():
    """Response all users from database"""
    users: list = User.get_all_existing()
    serializer: UserSchema = UserSchema(many=True)
    data: list = serializer.dump(users)
    return jsonify(data)


@app.route("/api/user", methods=["POST"])
def create_user():
    """Create new user in database"""
    data: list = request.get_json()
    new_user: User = User(
        name=data.get("name"),
        iin=data.get("iin"),
        email=data.get("email"),
        password=data.get("password")
    )

    new_user.save()
    serializer: UserRegisterSchema = UserRegisterSchema()
    data = serializer.dump(new_user)
    return jsonify(data), 201


@app.route("/api/user/<int:id>", methods=["GET"])
@auth.login_required
def retrieve_user(id: int):
    user = User.get_by_id(id)
    if not user:
        abort(404)
    
    serializer: UserSchema = UserSchema()
    data = serializer.dump(user)
    return jsonify(data), 200


@app.route("/api/user/<int:id>", methods=["PUT"])
@auth.login_required
def update_user(id: int):
    user_being_updated: User = User.get_by_id(id)
    if not user_being_updated:
        abort(404)

    data = request.get_json()
    user_being_updated.name = data.get("name")
    db.session.commit()

    serializer: UserSchema = UserSchema()
    data = serializer.dump(user_being_updated)
    return jsonify(data), 200


@app.route("/api/user/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_user(id: int):
    user_being_deleted: User = User.get_by_id(id)
    if not user_being_deleted:
        abort(404)

    user_being_deleted.delete()
    db.session.commit()
    return jsonify({
        "message": f"User {user_being_deleted.id} is deleted"
        }), 204


# ====

@app.route("/api/card", methods=["GET"])
@auth.login_required
def get_card_list():
    """Response all cards from database"""
    cards: list = Card.get_all_existing()
    serializer: CardSchema = CardSchema(many=True)
    data: list = serializer.dump(cards)
    return jsonify(data)


@app.route("/api/card", methods=["POST"])
@auth.login_required
def create_card():
    """Create new card in database"""
    data: list = request.get_json()
    user_id = data.get("owner_id")
    if Card.get_by_owner(user_id):
        return jsonify({"message": f"User {user_id} already have card"})

    new_card: Card = Card(
        owner_id=user_id,
        number=utils.generate_card_number(Card)
    )

    new_card.save()
    serializer: CardSchema = CardSchema()
    data = serializer.dump(new_card)
    return jsonify(data), 201


@app.route("/api/card/<int:id>", methods=["GET"])
@auth.login_required
def retrieve_card(id: int):
    card = Card.get_by_id(id)
    if not card:
        abort(404)

    serializer: CardSchema = CardSchema()
    data = serializer.dump(card)
    return jsonify(data), 200


@app.route("/api/card/<int:id>", methods=["PUT"])
@auth.login_required
def update_card(id: int):
    card_being_updated: Card = Card.get_by_id(id)
    if not card_being_updated:
        abort(404)

    data = request.get_json()
    card_being_updated.is_active = data.get("is_active")
    db.session.commit()

    serializer: CardSchema = CardSchema()
    data = serializer.dump(card_being_updated)
    return jsonify(data), 200


@app.route("/api/card/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_card(id: int):
    card_being_deleted: Card = Card.get_by_id(id)
    if not card_being_deleted:
        abort(404)

    card_being_deleted.delete()
    db.session.commit()
    return jsonify({
        "message": f"Card {card_being_deleted.id} is deleted"
        }), 204


@app.route("/api/card/<int:id>/block", methods=["GET"])
@auth.login_required
def block_card(id: int):
    card: Card = Card.get_active_by_id(id)
    card.is_active = False
    db.session.commit()

    serializer: CardSchema = CardSchema()
    data = serializer.dump(card)
    return jsonify(data)


@app.route("/api/card/change-card", methods=["POST"])
@auth.login_required
def change_card():
    data: list = request.get_json()
    user_id = data.get("owner_id")
    if Card.get_active_by_owner(user_id):
        return jsonify({"message": f"User {user_id} have active card"})

    old_card: Card = Card.get_by_owner(user_id)
    if not old_card:
        abort(404)
    old_card.delete()
    new_card: Card = Card(
        owner_id=user_id,
        number=utils.generate_card_number(Card)
    )

    new_card.save()
    serializer: CardSchema = CardSchema()
    data = serializer.dump(new_card)
    return jsonify(data), 201


@app.route("/api/pay", methods=["POST"])
@auth.login_required
def pay_with_card():
    start_time = time.time()
    data: dict = request.get_json()
    card_number = data.get("number")
    if card_number == "4111111111111111" or card_number == "4242424242424242":
        abort(403)
    
    card: Card = Card.get_by_number(card_number)
    current_date = datetime.strptime(data.get("validity_period"), "%Y-%m-%d").date()
    if not card or not card.is_active:
        abort(404)
    transaction: Transaction = Transaction(card_id=card.id)
    serializer: TransactionSchema = TransactionSchema()
    if card.cvv != data.get("cvv") \
        or card.validity_period != current_date:
        transaction.status = Status.bad
        data = serializer.dump(transaction)
        transaction.save()
        return jsonify(data), 400
    
    if time.time() - start_time > 8:
        transaction.status = Status.time
        transaction.save()
        data = serializer.dump(transaction)
        return jsonify(data), 200

    transaction.status = Status.ok
    transaction.save()
    data = serializer.dump(transaction)
    return jsonify(data), 200

    

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resourse not found"})


@app.errorhandler(500)
def not_found(error):
    return jsonify({"message": "Server is broke"})


if __name__ == "__main__":
    db.create_all()
    Generator().generation()
    app.run(debug=True, port="8080", host="0.0.0.0")
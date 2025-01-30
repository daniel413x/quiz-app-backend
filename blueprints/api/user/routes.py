import uuid

from flask import Blueprint, jsonify, request, make_response

from models.domain import Domain
from models.user import User
from utils.decode_jwt import decode_jwt
from extensions import db
# from models.serializers.user_get_many_serializer import UserGetManySerializer
import coolname

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        existing_user = User.query.filter_by(auth0_id=data["auth0Id"]).first()
        if existing_user:
            return make_response(jsonify({}))
        user_uuid = uuid.uuid4()
        user = User(email=data["email"], auth0_id=data["auth0Id"], id=user_uuid)
        db.session.add(user)
        domain = Domain()
        domain_name = coolname.generate()
        domain_slug = '-'.join(domain_name)
        domain.name = ' '.join(domain_name).capitalize()
        domain.slug = domain_slug
        domain.invited_users = [user_uuid]

        domain.user_id = user_uuid  # Set the user's ID in the domain
        user.domain = domain
        db.session.commit()
        return jsonify(user.json())
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating user", "error": str(e)}), 500
        )


# get a specific user
@user_bp.route("/by-token", methods=["GET"])
def get_user_by_auth0_id():
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        if user:
            return make_response(jsonify(user.json()), 200)
        return jsonify(make_response(jsonify({"message": "user not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting user", "error": str(e)}), 500
        )


# update a user
@user_bp.route("/<id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data["name"]
            db.session.commit()
            return make_response(jsonify({"message": "user updated"}), 204)
        return jsonify(make_response(jsonify({"message": "user not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating user", "error": str(e)}), 500
        )


# delete a user
@user_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 204)
        return jsonify(make_response(jsonify({"message": "user not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting user", "error": str(e)}), 500
        )

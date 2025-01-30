from flask import Blueprint, jsonify, request, make_response
from models.user import User
from models.domain import Domain
from extensions import db
import coolname

domain_bp = Blueprint("domain_bp", __name__)


@domain_bp.route("/", methods=["GET"])
def get_quiz_categories():
    try:
        load_quizzes = request.args.get("quizzes", "false").lower() == "true"
        # base query, eagerly load domain
        query = QuizCategory.query.options(db.joinedload(QuizCategory.domain))
        # add eager loading for quizzes
        # if the param is true
        if load_quizzes:
            # explicitly eager-load quizzes when requested
            query = query.options(db.joinedload(QuizCategory.quizzes))
        else:
            # explicitly set lazy='noload' to prevent quizzes from being accessed
            query = query.options(db.noload(QuizCategory.quizzes))
        quiz_category = query.all()
        serializer = QuizCategoryGetManySerializer(many=True)
        quizzes = serializer.dump(quiz_category)
        return jsonify(quizzes, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz_category", "error": str(e)}), 500
        )



# get a specific domain
@domain_bp.route("/by-auth0-id/<id>", methods=["GET"])
def get_domain(id):
    try:
        user = User.query.filter_by(auth0_id=id).first()
        domain = Domain.query.filter_by(user_id=user.id).first()
        if domain:
            return make_response(jsonify({"domain": domain.json()}), 200)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting domain", "error": str(e)}), 500
        )


# update a domain
@domain_bp.route("/<id>", methods=["PUT"])
def update_domain(id):
    try:
        domain = Domain.query.filter_by(id=id).first()
        if domain:
            data = request.get_json()
            domain.name = data["name"]
            db.session.commit()
            return make_response(jsonify({"message": "domain updated"}), 204)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating domain", "error": str(e)}), 500
        )


# delete a domain
@domain_bp.route("/<id>", methods=["DELETE"])
def delete_domain(id):
    try:
        domain = Domain.query.filter_by(id=id).first()
        if domain:
            db.session.delete(domain)
            db.session.commit()
            return make_response(jsonify({"message": "domain deleted"}), 204)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting domain", "error": str(e)}), 500
        )

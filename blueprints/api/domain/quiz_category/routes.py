from flask import Blueprint, jsonify, request, make_response

from models.domain import Domain
from models.quiz_category import QuizCategory
from models.quiz import Quiz
from models.serializers.quiz_category_get_many_serializer import QuizCategoryGetManySerializer
from models.serializers.quiz_category_serializer import QuizCategorySerializer
from models.serializers.quiz_get_many_serializer import QuizGetManySerializer
from extensions import db

domain_quiz_category_bp = Blueprint("domain_quiz_category_bp", __name__)


@domain_quiz_category_bp.route("", methods=["GET"])
def get_quiz_categories(domain_slug):
    try:
        # TODO: add invited_users check if the domain is set to private
        domain = Domain.query.filter_by(slug=domain_slug).first_or_404()
        load_quizzes = request.args.get("quizzes", "false").lower() == "true"
        # base query, eagerly load domain
        query = QuizCategory.query.filter_by(domain_id=domain.id).options(db.joinedload(QuizCategory.domain))
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


@domain_quiz_category_bp.route("/<quiz_category_slug>", methods=["GET"])
def get_quiz_by_quiz_slug(quiz_category_slug, domain_slug):
    try:
        quiz_category_queried = QuizCategory.query.filter_by(slug=quiz_category_slug).first_or_404()
        serializer = QuizCategorySerializer()
        quiz_category = serializer.dump(quiz_category_queried)
        return jsonify(quiz_category)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quizzes by category name", "error": str(e)}), 500
        )


@domain_quiz_category_bp.route("/quizzes/<quiz_category_slug>", methods=["GET"])
def get_quizzes_by_quiz_slug(quiz_category_slug, domain_slug):
    try:
        quiz_category = QuizCategory.query.filter_by(slug=quiz_category_slug).first_or_404()
        queried_quizzes = Quiz.query.filter(Quiz.category_id == quiz_category.id).all()
        serializer = QuizGetManySerializer()
        quizzes = serializer.dump(queried_quizzes, many=True)
        return jsonify(quizzes)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quizzes by category name", "error": str(e)}), 500
        )

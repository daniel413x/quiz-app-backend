from flask import Blueprint, jsonify, make_response
from models.quiz import Quiz
from models.serializers.quiz_serializer import QuizSerializer

domain_quiz_bp = Blueprint("domain_quiz_bp", __name__)


@domain_quiz_bp.route("/<quiz_slug>", methods=["GET"])
def get_quiz_by_quiz_slug(quiz_slug, domain_slug):
    try:
        queried_quiz = Quiz.query.filter_by(slug=quiz_slug).first_or_404()
        serializer = QuizSerializer()
        quiz = serializer.dump(queried_quiz)
        return jsonify(quiz)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quizzes by category name", "error": str(e)}), 500
        )


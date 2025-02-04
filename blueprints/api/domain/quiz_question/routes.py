from flask import Blueprint, jsonify, request, make_response
from models.quiz import Quiz
from models.quiz_answer import QuizAnswer
from models.quiz_question import QuizQuestion
from extensions import db
from models.serializers.quiz_question_get_many_serializer import QuizQuestionGetManySerializer
from models.serializers.quiz_question_serializer import QuizQuestionSerializer
from models.user import User
from models.quiz_category import QuizCategory
from marshmallow import ValidationError

from utils.decode_jwt import decode_jwt

domain_quiz_question_bp = Blueprint("domain_quiz_question_bp", __name__)

# get quiz questions by quiz slug
@domain_quiz_question_bp.route("/get-by-quiz-slug/<quiz_slug>", methods=["GET"])
def get_quiz_questions_by_quiz_slug(quiz_slug):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz = Quiz.query.filter_by(slug=quiz_slug).first_or_404()
        category = QuizCategory.query.filter_by(id=quiz.category_id).first_or_404()
        if category.domain.id != user.domain.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
        quiz_questions_queried = QuizQuestion.query.join(Quiz).filter(Quiz.slug == quiz_slug).all()
        serializer = QuizQuestionGetManySerializer()
        quiz_questions = serializer.dump(quiz_questions_queried, many=True)
        return jsonify(quiz_questions, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )


# get a specific quiz question
@domain_quiz_question_bp.route("/<id>", methods=["GET"])
def get_quiz(id):
    try:
        query = QuizQuestion.query.filter_by(id=id).first()
        quiz = QuizQuestionSerializer().dump(query)
        if quiz:
            return make_response(jsonify(quiz), 200)
        return jsonify(make_response(jsonify({"message": "quiz not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )

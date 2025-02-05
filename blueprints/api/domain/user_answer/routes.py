import random
import uuid
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy.orm import joinedload

from models.quiz_instance import QuizInstance

from models.quiz_answer import QuizAnswer
from models.quiz_instance_answer import QuizInstanceAnswer
from extensions import db
from models.quiz_instance_question import QuizInstanceQuestion
from models.quiz_results import QuizResults
from models.serializers.quiz_instance_question_serializer import QuizInstanceQuestionSerializer
from models.user_answer import UserAnswer

domain_user_answer_bp = Blueprint("domain_user_answer_bp", __name__)


@domain_user_answer_bp.route("", methods=["POST"])
def create_user_answer(domain_slug, instance_id):
    try:
        data = request.get_json()
        # answer_id refers to a quiz_instance_answer
        answer_id = data["answerId"]
        quiz_instance_answer = QuizInstanceAnswer.query.filter_by(id=answer_id).first_or_404()
        quiz_answer = QuizAnswer.query.filter_by(id=quiz_instance_answer.quiz_answer_id).first_or_404()
        is_correct = quiz_answer.correct_answer
        existing_user_answer = UserAnswer.query.filter_by(quiz_instance_answer_id=answer_id).first()
        if existing_user_answer:
            return jsonify({ "is_correct": is_correct }), 200
        will_increment_progress = is_correct and not existing_user_answer
        if will_increment_progress:
            quiz_results = QuizResults.query.filter_by(quiz_instance_id=instance_id).first_or_404()
            quiz_results.progress += 1
        user_answer = UserAnswer()
        user_answer.quiz_instance_answer_id = answer_id
        db.session.add(user_answer)
        db.session.commit()
        return jsonify({ "is_correct": is_correct }), 200
    except Exception as e:
        print(e)
        # Handle other exceptions
        return make_response(
            jsonify({"message": "Error creating user answer", "error": str(e)}), 500
        )


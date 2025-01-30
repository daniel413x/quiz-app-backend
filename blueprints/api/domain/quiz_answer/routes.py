from flask import Blueprint, jsonify, request, make_response
from models.quiz import Quiz
from extensions import db
from models.quiz_answer import QuizAnswer

domain_quiz_answer_bp = Blueprint("domain_quiz_answer_bp", __name__)


@domain_quiz_answer_bp.route("", methods=["POST"])
def create_quiz():
    try:
        data = request.get_json()
        answers = data["answers"]
        new_quiz = QuizAnswer()
        db.session.add(new_quiz)
        db.session.commit()
        return jsonify(
            {
                "id": new_quiz.id,
                "name": new_quiz.name,
                "email": new_quiz.email,
            }
        )
    except Exception as e:
        return make_response(

            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )


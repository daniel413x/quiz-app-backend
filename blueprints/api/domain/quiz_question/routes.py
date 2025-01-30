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

@domain_quiz_question_bp.route("", methods=["POST"])
def create_quiz_question():
    try:
        data = request.get_json()
        quiz_question_schema = QuizQuestionSerializer()
        answers = data.get("answers", [])
        quiz_slug = data.get("quizSlug")
        quiz = Quiz.query.filter(Quiz.slug == quiz_slug).first_or_404()
        question_data = {
            "question": data["question"],
            "answers": answers  # Add the deserialized answers to the question
        }
        new_quiz_question = quiz_question_schema.load(question_data)
        new_quiz_question.quiz_id = quiz.id
        db.session.add(new_quiz_question)
        db.session.commit()
        result = quiz_question_schema.dump(new_quiz_question)
        return jsonify(result), 201
    except ValidationError as e:
        # Handle validation errors
        return make_response(jsonify({"message": "Validation error", "errors": e.messages}), 400)

    except Exception as e:
        # Handle other exceptions
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )


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


# update a quiz
@domain_quiz_question_bp.route("/<question_id>", methods=["PUT"])
def update_quiz_question(question_id):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz_question = QuizQuestion.query.get_or_404(question_id)
        if quiz_question.domain.id != user.domain.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
        data = request.get_json()
        quiz_slug = data.get("quizSlug")
        quiz = Quiz.query.filter(Quiz.slug == quiz_slug).first_or_404()
        quiz_question.question = data["question"]
        quiz_question.quiz_id = quiz.id
        answers_data = data.get("answers", [])
        # determine deleted answers
        # then delete them
        quiz_answers = QuizAnswer.query.filter(QuizAnswer.quiz_question_id == question_id).all()
        form_answer_ids = []
        for answer in answers_data:
            form_answer_ids.append(answer["id"])
        deleted_answer_ids = []
        for answer in quiz_answers:
            if answer.id not in form_answer_ids:
                deleted_answer_ids.append(answer.id)
        QuizAnswer.query.filter(QuizAnswer.id.in_(deleted_answer_ids)).delete(synchronize_session="fetch")
        for form_answer in answers_data:
            existing_answer = QuizAnswer.query.filter_by(id=form_answer["id"]).first()
            if existing_answer:
                existing_answer.answer = form_answer.get("answer")
                existing_answer.correct_answer = form_answer.get("correctAnswer")
                existing_answer.order = form_answer.get("order")
            else:
                # Create a new answer
                new_answer = QuizAnswer(
                    answer=form_answer.get("answer"),
                    correct_answer=form_answer.get("correctAnswer"),
                    order=form_answer.get("order"),
                    quiz_question_id=quiz_question.id,
                )
                db.session.add(new_answer)
        db.session.commit()
        return make_response(jsonify({}), 204)
    except ValidationError as e:
        # Handle validation errors
        return make_response(jsonify({"message": "Validation error", "errors": e.messages}), 400)
    except Exception as e:
        # Handle other exceptions
        return make_response(
            jsonify({"message": "Error updating quiz question", "error": str(e)}), 500
        )


# delete a quiz
@domain_quiz_question_bp.route("/<id>", methods=["DELETE"])
def delete_quiz(id):
    try:
        quiz_question = QuizQuestion.query.filter_by(id=id).first_or_404()
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz = Quiz.query.filter_by(id=quiz_question.quiz_id).first()
        category = QuizCategory.query.filter_by(id=quiz.category_id).first()
        if quiz and category:
            if category.domain.id != user.domain.id:
                return make_response(
                    jsonify({"message": "Domain mismatch"}),
                    403
                )
        else:
            raise Exception("Relational objects were missing")
        db.session.delete(quiz_question)
        db.session.commit()
        return make_response(jsonify({"message": "quiz question deleted"}), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting quiz question", "error": str(e)}), 500
        )

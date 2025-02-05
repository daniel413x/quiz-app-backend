import random
import uuid
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy.orm import joinedload

from models.quiz import Quiz
from models.quiz_answer import QuizAnswer
from models.quiz_instance_answer import QuizInstanceAnswer
from models.quiz_instance_question import QuizInstanceQuestion
from models.quiz_question import QuizQuestion
from models.quiz_instance import QuizInstance
from extensions import db
from models.quiz_results import QuizResults
from models.serializers.quiz_instance_question_serializer import QuizInstanceQuestionSerializer
from models.serializers.quiz_instance_serializer import QuizInstanceSerializer
from models.user_answer import UserAnswer

domain_quiz_instance_bp = Blueprint("domain_quiz_instance_bp", __name__)



@domain_quiz_instance_bp.route("/<id>", methods=["GET"])
def get_quiz_instance(domain_slug, id):
    try:
        query = QuizInstance.query.filter_by(id=id).options(
            joinedload(QuizInstance.questions)
            .joinedload(QuizInstanceQuestion.answers)
        ).first_or_404()
        serializer = QuizInstanceSerializer()
        quiz_instance = serializer.dump(query)
        return jsonify(quiz_instance), 200
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )



@domain_quiz_instance_bp.route("", methods=["POST"])
def create_quiz_instance(domain_slug):
    try:
        # fetch Quiz, create QuizInstance
        data = request.get_json()
        quiz_slug = data["quizSlug"]
        quiz = Quiz.query.filter_by(slug=quiz_slug).first_or_404()
        quiz_instance = QuizInstance()
        quiz_instance.quiz_id = quiz.id
        quiz_instance_id = uuid.uuid4()
        quiz_instance.id = quiz_instance_id
        db.session.add(quiz_instance)
        # handle randomized question generation
        quiz_questions_queried = QuizQuestion.query.join(Quiz).filter(Quiz.slug == quiz_slug).all()
        randomized_quiz_questions = random.sample(quiz_questions_queried, 26)
        for question in randomized_quiz_questions:
            new_quiz_instance_question_id = uuid.uuid4()
            new_quiz_instance_question = QuizInstanceQuestion()
            new_quiz_instance_question.id = new_quiz_instance_question_id
            new_quiz_instance_question.quiz_question_id = question.id
            new_quiz_instance_question.quiz_instance_id = quiz_instance_id
            new_quiz_instance_question.question = question.question
            quiz_answers_queried = QuizAnswer.query.join(QuizQuestion).filter(QuizQuestion.id == question.id).all()
            for answer in quiz_answers_queried:
                new_quiz_instance_answer = QuizInstanceAnswer()
                new_quiz_instance_answer.quiz_answer_id = answer.id
                new_quiz_instance_answer.quiz_instance_id = quiz_instance_id
                new_quiz_instance_answer.answer = answer.answer
                new_quiz_instance_answer.correct_answer = answer.correct_answer
                new_quiz_instance_answer.quiz_instance_question_id = new_quiz_instance_question_id
                db.session.add(new_quiz_instance_answer)
            db.session.add(new_quiz_instance_question)
        quiz_results = QuizResults()
        quiz_results.quiz_instance_id = quiz_instance_id
        db.session.add(quiz_results)
        db.session.commit()
        # return only the idea which the FE uses to push to the next page
        return jsonify({ "id": str(quiz_instance_id) }), 200
    except Exception as e:
        print(e)
        # Handle other exceptions
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )


@domain_quiz_instance_bp.route("/<id>/get-quiz-question/<q_num>", methods=["GET"])
def get_quiz_instance_question(domain_slug, id, q_num):
    """
    get a quiz question by id and integer

    as the user works through a quiz, they will query the endpoint and use the param qNum incrementally, e.g. 1, 2, 3, etc.

    if the user tries to access a quiz question that they have not yet progressed to, return a number according to their actual progress
    """
    try:
        quiz_results = QuizResults.query.filter_by(quiz_instance_id=id).first_or_404()
        if int(q_num) > quiz_results.progress:
            return jsonify({ "redirect": str(quiz_results.progress) }), 200
        query = QuizInstance.query.filter_by(id=id).options(
            joinedload(QuizInstance.questions)
            .joinedload(QuizInstanceQuestion.answers)
        )
        instance = query.first()
        quiz_question = instance.questions[int(q_num)]
        # get answer IDs from QuizInstanceAnswers
        answer_ids = [answer.id for answer in quiz_question.answers]
        # find correct QuizInstanceAnswers where the original QuizAnswer is marked correct
        correct_quiz_instance_answers = QuizInstanceAnswer.query.join(QuizAnswer).filter(
            QuizInstanceAnswer.id.in_(answer_ids),
            QuizAnswer.correct_answer == True
        ).all()
        # find a UserAnswer that matches these correct answers
        # on the frontend, will be used to immediately mark the answer correct if the user is navigating back through questions they already passed
        correct_user_answer = UserAnswer.query.filter(
            UserAnswer.quiz_instance_answer_id.in_([ans.id for ans in correct_quiz_instance_answers])
        ).first()
        # serialize
        serializer = QuizInstanceQuestionSerializer()
        returned_question = serializer.dump(quiz_question)
        # include the correct user answer if found
        if correct_user_answer:
            returned_question["correct_user_answer"] = correct_user_answer.json()
        return jsonify(returned_question), 200
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )

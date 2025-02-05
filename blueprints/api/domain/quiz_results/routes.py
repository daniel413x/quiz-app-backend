from flask import Blueprint, jsonify, make_response

from models.quiz_results import QuizResults

domain_quiz_results_bp = Blueprint("domain_quiz_results_bp", __name__)

@domain_quiz_results_bp.route("/<instance_id>", methods=["GET"])
def get_quiz_results_question(domain_slug, instance_id):
    """
    get quiz results

    quiz results are used to render a % progress tracker while taking a quiz
    """
    try:
        quiz_results = QuizResults.query.filter_by(quiz_instance_id=instance_id).first_or_404()
        return jsonify(quiz_results.json()), 200
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )

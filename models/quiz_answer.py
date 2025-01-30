import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizAnswer(db.Model):
    __tablename__ = "quiz_answer"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    correct_answer = db.Column(db.Boolean, nullable=False)

    order = db.Column(db.Integer, nullable=True)

    # Foreign key to QuizQuestion
    quiz_question_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz_question.id'), nullable=False)

    # Relationship to question
    question = db.relationship('QuizQuestion', back_populates='answers')

    def json(self):
        return {
            "id": str(self.id),
            "answer": self.answer,
        }



# update a quiz
# @quiz_question_bp.route("/<question_id>", methods=["PUT"])
# def update_quiz_question(question_id):
#     try:
#         data = request.get_json()
#         quiz_question = QuizQuestion.query.get_or_404(question_id)
#         quiz_slug = data.get("quizSlug")
#         quiz = Quiz.query.filter(Quiz.slug == quiz_slug).first_or_404()
#         quiz_question.question = data["question"]
#         quiz_question.quiz_id = quiz.id
#         answers_data = data.get("answers", [])
#         print(answers_data)
#         # determine deleted answers
#         # then delete them
#         # quiz_answers = QuizAnswer.query.filter(QuizAnswer.quiz_question_id == question_id).all()
#         # print(quiz_answers)
#         # form_answer_ids = []
#         # for answer in answers_data:
#         #     form_answer_ids.append(answer["id"])
#         # deleted_answer_ids = []
#         # for answer in quiz_answers:
#         #     if answer.id not in form_answer_ids:
#         #         deleted_answer_ids.append(answer.id)
#         # QuizAnswer.query.filter(QuizAnswer.id.in_(deleted_answer_ids)).delete(synchronize_session="fetch")
#         for form_answer in answers_data:
#             if "id" in form_answer:
#                 # Update existing answer
#                 existing_answer = QuizAnswer.query.filter_by(id=form_answer["id"]).first()
#                 if existing_answer:
#                     existing_answer.answer = form_answer.get("answer")
#                     existing_answer.correct_answer = form_answer.get("correctAnswer")
#                     existing_answer.order = form_answer.get("order")
#                 else:
#                     raise Exception(f"Answer with id {form_answer['id']} not found.")
#             else:
#                 # Create a new answer
#                 new_answer = QuizAnswer(
#                     answer=form_answer.get("answer"),
#                     correct_answer=form_answer.get("correctAnswer"),
#                     order=form_answer.get("order"),
#                     quiz_question_id=quiz_question.id,
#                 )
#                 db.session.add(new_answer)
#
#         db.session.commit()
#         return make_response(jsonify({}), 204)

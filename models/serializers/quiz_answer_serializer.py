from marshmallow import Schema, fields, post_load
from models.quiz_answer import QuizAnswer


class QuizAnswerSerializer(Schema):
    id = fields.UUID(data_key="id")  # UUID will be auto-generated if not provided
    answer = fields.Str(data_key="answer")
    correct_answer = fields.Bool(data_key="correctAnswer")  # Map 'correctAnswer' to 'correct_answer'
    order = fields.Int(data_key="order", allow_none=True)
    quiz_question_id = fields.UUID(data_key="quizQuestionId", allow_none=True)  # Map 'quizQuestionId' to 'quiz_question_id'

    @post_load
    def make_quiz_answer(self, data, **kwargs):
        """Convert the deserialized data into a QuizAnswer model instance."""
        return QuizAnswer(**data)


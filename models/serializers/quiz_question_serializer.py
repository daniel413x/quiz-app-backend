from marshmallow import Schema, fields, post_load
from models.serializers.quiz_answer_serializer import QuizAnswerSerializer
from models.quiz_question import QuizQuestion


class QuizQuestionSerializer(Schema):
    id = fields.UUID(data_key="id")
    question = fields.Str(data_key="question")
    quiz_id = fields.UUID(data_key="quizId", required=False)
    answers = fields.Nested(QuizAnswerSerializer, many=True)  # serialize nested answers

    @post_load
    def make_quiz_question(self, data, **kwargs):
        return QuizQuestion(**data)

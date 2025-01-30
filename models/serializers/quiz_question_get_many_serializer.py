from marshmallow import Schema, fields, post_load
from models.serializers.quiz_answer_serializer import QuizAnswerSerializer
from models.quiz_question import QuizQuestion


class QuizQuestionGetManySerializer(Schema):
    id = fields.UUID(data_key="id")
    question = fields.Str(data_key="question")

    @post_load
    def make_quiz_question(self, data, **kwargs):
        return QuizQuestion(**data)

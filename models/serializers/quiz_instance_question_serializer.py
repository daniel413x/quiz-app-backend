from marshmallow import Schema, fields, post_load
from models.serializers.quiz_answer_serializer import QuizAnswerSerializer
from models.quiz_instance_question import QuizInstanceQuestion

class QuizInstanceAnswerSerializer(Schema):
    id = fields.UUID(data_key="id")
    answer = fields.Str(data_key="answer")
    quiz_answer_id = fields.UUID(data_key="quizAnswerId")

class QuizInstanceQuestionSerializer(Schema):
    id = fields.UUID(data_key="id")
    question = fields.Str(data_key="question")
    quiz_instance_id = fields.UUID(data_key="quizInstanceId")
    answers = fields.Nested(QuizInstanceAnswerSerializer, many=True)  # serialize nested answers

    @post_load
    def make_quiz_instance_question(self, data, **kwargs):
        return QuizInstanceQuestion(**data)

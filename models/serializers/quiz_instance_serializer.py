from marshmallow import Schema, fields, post_load
from models.quiz_instance_question import QuizInstanceQuestion
from models.quiz_instance_answer import QuizInstanceAnswer
from models.user_answer import UserAnswer
from models.quiz_answer import QuizAnswer


class UserAnswerSerializer(Schema):
    id = fields.UUID(data_key="id")
    quiz_instance_answer_id = fields.UUID(data_key="quizInstanceAnswerId")

    @post_load
    def make_user_answer(self, data, **kwargs):
        return UserAnswer(**data)


class QuizAnswerSerializer(Schema):
    correct_answer = fields.Bool(data_key="correctAnswer")

    @post_load
    def make_quiz_answer(self, data, **kwargs):
        return QuizAnswer(**data)


class QuizInstanceAnswerSerializer(Schema):
    id = fields.UUID(data_key="id")
    answer = fields.Str(data_key="answer")

    quiz_answer = fields.Nested(QuizAnswerSerializer, data_key="quizAnswer")

    user_answer = fields.Nested(UserAnswerSerializer, data_key="userAnswer")

    @post_load
    def make_quiz_instance_answer(self, data, **kwargs):
        return QuizInstanceAnswer(**data)


class QuizInstanceQuestionSerializer(Schema):
    id = fields.UUID(data_key="id")
    question = fields.Str(data_key="question")
    quiz_instance_id = fields.UUID(data_key="quizInstanceId")
    answers = fields.Nested(QuizInstanceAnswerSerializer, many=True)  # Serialize nested answers

    @post_load
    def make_quiz_instance_question(self, data, **kwargs):
        return QuizInstanceQuestion(**data)


class QuizInstanceSerializer(Schema):
    id = fields.UUID(data_key="id")
    questions = fields.Nested(QuizInstanceQuestionSerializer, many=True)

    @post_load
    def make_quiz_instance_question(self, data, **kwargs):
        return QuizInstanceQuestion(**data)

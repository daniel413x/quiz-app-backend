from marshmallow import Schema, fields, post_load, EXCLUDE
from models.quiz_category import QuizCategory


class DomainSerializer(Schema):
    id = fields.UUID()
    name = fields.Str()
    slug = fields.Str()


class QuizSerializer(Schema):
    id = fields.UUID()
    name = fields.Str()
    slug = fields.Str()


class QuizCategoryGetManySerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)
    domain = fields.Nested(DomainSerializer, required=False)
    quizzes = fields.Nested(QuizSerializer, many=True, required=False, default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_quiz_category(self, data, **kwargs):
        return QuizCategory(**data)

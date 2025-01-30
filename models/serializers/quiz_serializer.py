from marshmallow import Schema, fields, post_load
from models.quiz import Quiz


class QuizSerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)  # UUID will be auto-generated if not provided
    name = fields.Str(required=True)
    slug = fields.Str(required=True)

    @post_load
    def make_quiz(self, data, **kwargs):
        return Quiz(**data)


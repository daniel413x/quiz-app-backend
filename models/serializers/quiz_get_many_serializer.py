from marshmallow import Schema, fields, post_load
from models.quiz import Quiz


class QuizGetManySerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)  # UUID will be auto-generated if not provided
    name = fields.Str(required=True)  # Quiz name is required
    slug = fields.Str(required=True)  # Quiz name is required

    @post_load
    def make_quiz(self, data, **kwargs):
        return Quiz(**data)

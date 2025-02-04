from marshmallow import Schema, fields, post_load
from models.serializers.quiz_serializer import QuizSerializer
from models.quiz_category import QuizCategory


class QuizCategorySerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)  # UUID will be auto-generated if not provided
    name = fields.Str(required=True)  # Category name is required

    @post_load
    def make_quiz_category(self, data, **kwargs):
        return QuizCategory(**data)

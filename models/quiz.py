import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)

    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz_category.id'), nullable=False)

    category = db.relationship('QuizCategory', back_populates='quizzes')

    questions = db.relationship('QuizQuestion', back_populates='quiz', cascade="all, delete", lazy=True)
    quiz_instances = db.relationship("QuizInstance", cascade="all, delete", lazy=True)

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "category_id": str(self.category_id),
        }

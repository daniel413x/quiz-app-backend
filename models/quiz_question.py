import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizQuestion(db.Model):
    __tablename__ = "quiz_question"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    question = db.Column(db.Text, nullable=False)

    # Foreign key to Quiz
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz.id'), nullable=False)

    # Relationship: A question has many answers
    answers = db.relationship('QuizAnswer', back_populates='question', cascade="all, delete-orphan", lazy=True)

    # Relationship to quiz
    quiz = db.relationship('Quiz', back_populates='questions')

    def json(self):
        return {
            "id": str(self.id),
            "question": self.question,
        }

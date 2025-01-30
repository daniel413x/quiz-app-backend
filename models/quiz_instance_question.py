import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizInstanceQuestion(db.Model):
    __tablename__ = "quiz_instance_question"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    quiz_instance_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_instance.id"), nullable=False)
    quiz_question_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_question.id"), nullable=False)

    answers = db.relationship('QuizInstanceAnswer', back_populates='quiz_instance_question', cascade="all, delete-orphan", lazy=True)
    quiz_instance = db.relationship("QuizInstance", back_populates="questions")
    quiz_question = db.relationship("QuizQuestion")

    question = db.Column(db.String, nullable=False)

    def json(self):
        return {
            "id": str(self.id),
            "quiz_instance_id": str(self.quiz_instance_id),
            "quiz_question_id": str(self.quiz_question_id),
        }
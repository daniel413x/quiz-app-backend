import uuid


from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizInstance(db.Model):
    __tablename__ = "quiz_instance"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz.id", ondelete="SET NULL"), nullable=True)

    quiz = db.relationship("Quiz", back_populates="quiz_instances")
    questions = db.relationship("QuizInstanceQuestion", cascade="all, delete", back_populates="quiz_instance")

    def json(self):
        return {
            "id": str(self.id),
        }

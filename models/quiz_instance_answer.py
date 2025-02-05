import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizInstanceAnswer(db.Model):
    __tablename__ = "quiz_instance_answer"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    quiz_instance_question_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_instance_question.id"), nullable=False)
    quiz_answer_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_answer.id", ondelete="SET NULL"), nullable=True)
    answer = db.Column(db.String, nullable=False)

    user_answer = db.relationship("UserAnswer", back_populates="quiz_instance_answer", uselist=False)

    quiz_instance_question = db.relationship("QuizInstanceQuestion")
    quiz_answer = db.relationship("QuizAnswer", back_populates="quiz_instance_answer", lazy=True)

    def json(self):
        return {
            "id": str(self.id),
            "quiz_instance_question_id": str(self.quiz_instance_question_id),
            "quiz_answer_id": str(self.quiz_answer_id) if self.quiz_answer_id else None,
            "correct": self.correct,
        }
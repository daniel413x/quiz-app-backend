import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class UserAnswer(db.Model):
    __tablename__ = "user_answer"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    quiz_instance_answer_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_instance_answer.id"), nullable=True)

    quiz_instance_answer = db.relationship("QuizInstanceAnswer")

    # quiz_instance_question_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz_instance_question.id"), nullable=True)
    #
    # quiz_instance_question = db.relationship("QuizInstanceQuestion")

    def json(self):
        return {
            "id": str(self.id),
            "quiz_instance_answer_id": str(self.quiz_instance_answer_id),
        }
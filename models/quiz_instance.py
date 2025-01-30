import uuid


from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizInstance(db.Model):
    __tablename__ = "quiz_instance"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quiz.id"), nullable=False)

    quiz = db.relationship("Quiz", back_populates="quiz_instances")
    questions = db.relationship("QuizInstanceQuestion", cascade="all, delete", back_populates="quiz_instance")

    # fetch all quiz_instance_question
    # access the array by question param page number
    # on rendering results, you can just fetch all of them
    # and on rendering results, it should be possible to populate quiz_instance_answer to the quiz_instance_questions
    # on the FE, map through the populated quiz_instance_answer and style according the boolean is correct or not

    def json(self):
        return {
            "id": str(self.id),
        }

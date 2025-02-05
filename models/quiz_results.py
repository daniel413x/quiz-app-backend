import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizResults(db.Model):
    __tablename__ = "quiz_results"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    progress = db.Column(db.Integer, nullable=False, default=0)

    quiz_instance_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz_instance.id'), nullable=False)

    def json(self):
        return {
            "id": str(self.id),
            "progress": str(self.progress),
        }


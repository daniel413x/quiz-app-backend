import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizCategory(db.Model):
    __tablename__ = "quiz_category"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    # uniqueness should be enforced within domains
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False)

    # Foreign key to Domain
    domain_id = db.Column(UUID(as_uuid=True), db.ForeignKey("domain.id"), nullable=False)

    # Relationship: A category belongs to one domain
    domain = db.relationship("Domain", back_populates="quiz_categories")

    # Relationship: A category has many quizzes
    quizzes = db.relationship('Quiz', back_populates='category', cascade="all, delete", lazy=True)

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.name,
            "domain_id": str(self.domain_id),
        }

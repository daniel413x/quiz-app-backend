import uuid


from extensions import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY


class Domain(db.Model):
    __tablename__ = "domain"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="domain")

    private = db.Column(db.Boolean, default=False)

    invited_users = db.Column(ARRAY(db.String), default=[])

    quiz_categories = db.relationship("QuizCategory", cascade="all, delete", lazy=True, back_populates='domain')

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "private": self.private,
            "invited_users": self.invited_users,
            "user_id": self.user_id,
        }

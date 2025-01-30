import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    auth0_id = db.Column(db.String(), unique=True, nullable=False)
    domain = db.relationship("Domain", back_populates="user", uselist=False)

    def json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "auth0_id": self.auth0_id,
            "domain": self.domain.json(),
        }

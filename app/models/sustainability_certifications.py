from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class SustainabilityCertification(db.Model):
    __tablename__ = "sustainability_certifications"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=True)
    icon: Mapped[str] = mapped_column(db.String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

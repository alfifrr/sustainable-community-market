from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Address(db.Model):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    label: Mapped[str] = mapped_column(db.String(50), nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    details: Mapped[str] = mapped_column(db.String(255), nullable=True)
    contact_person: Mapped[str] = mapped_column(db.String(255), nullable=False)

    date_created: Mapped[datetime] = mapped_column(db.DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc))
    date_updated: Mapped[datetime] = mapped_column(db.DateTime(
        timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    # FK
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Rel
    user = db.relationship('User', back_populates='addresses')

    def __repr__(self):
        return f'<Address {self.label} for user {self.user_id}'

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "address": self.address,
            "details": self.details,
            "contact_person": self.contact_person,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
            "user_id": self.user_id
        }

from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum


class CertificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProductCertification(db.Model):
    __tablename__ = "product_certifications"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    status: Mapped[CertificationStatus] = mapped_column(
        db.Enum(CertificationStatus),
        nullable=False,
        default=CertificationStatus.PENDING,
    )
    verification_date: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Foreign Keys
    product_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    certification_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey("sustainability_certifications.id", ondelete="CASCADE"),
        nullable=False,
    )
    verified_by: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    product = db.relationship(
        "Product", backref=db.backref("certifications", lazy=True), lazy=True
    )
    certification = db.relationship(
        "SustainabilityCertification",
        backref=db.backref("products", lazy=True),
        lazy=True,
    )
    verifier = db.relationship(
        "User", backref=db.backref("verified_certifications", lazy=True), lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status.value,
            "verification_date": (
                self.verification_date.isoformat() if self.verification_date else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "product": (
                {"id": self.product.id, "name": self.product.name}
                if self.product
                else None
            ),
            "certification": (
                {"id": self.certification.id, "name": self.certification.name}
                if self.certification
                else None
            ),
            "verifier": (
                {
                    "id": self.verifier.id,
                    "name": f"{self.verifier.first_name} {self.verifier.last_name}",
                }
                if self.verifier
                else None
            ),
        }

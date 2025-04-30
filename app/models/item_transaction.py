from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum


class StatusType(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"
    RATED = "rated"


class ItemTransaction(db.Model):
    __tablename__ = "item_transactions"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    original_price: Mapped[float] = mapped_column(
        db.Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(
        db.Numeric(10, 2), nullable=False)
    pickup_address_details = db.Column(db.JSON, nullable=False)
    delivery_address_details = db.Column(db.JSON, nullable=False)
    delivery_status: Mapped[StatusType] = mapped_column(
        db.Enum(StatusType), nullable=False, default=StatusType.PENDING
    )
    product_details = db.Column(db.JSON, nullable=False)

    rating: Mapped[int] = mapped_column(
        db.Integer, nullable=True, comment="Rating from buyer to seller (1-5)"
    )
    testimonial: Mapped[str] = mapped_column(
        db.String(1000), nullable=True, comment='Product review text from the buyer'
    )
    review_date: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=True, comment="Timestamp when review was submitted"
    )

    # FK
    product_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("products.id", ondelete='SET NULL'), nullable=True
    )
    pickup_address_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("addresses.id"), nullable=False
    )
    delivery_address_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("addresses.id"), nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    buyer_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    # rel
    product = db.relationship(
        "Product", backref="transactions", passive_deletes=True)
    seller = db.relationship(
        "User",
        foreign_keys=[seller_id],
        backref=db.backref("seller_transactions", lazy="dynamic"),
    )
    buyer = db.relationship(
        "User",
        foreign_keys=[buyer_id],
        backref=db.backref("buyer_transactions", lazy="dynamic"),
    )

    def submit_review(self, rating: int, testimonial: str | None) -> None:
        self.rating = rating
        self.testimonial = testimonial
        self.review_date = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "quantity": self.quantity,
            "total_price": float(self.total_price) if self.total_price else 0.0,
            "pickup_address_details": self.pickup_address_details or {},
            "delivery_address_details": self.delivery_address_details or {},
            "product_details": self.product_details or {},
            "delivery_status": (
                self.delivery_status.value
                if self.delivery_status
                else StatusType.PENDING.value
            ),
            "rating": self.rating,
            "testimonial": self.testimonial,
            "review_date": self.review_date,
            "product": {"id": self.product.id, "name": self.product.name} if self.product else None,
            "seller": (
                {
                    "id": self.seller.id,
                    "name": f"{self.seller.first_name} {self.seller.last_name}",
                }
                if self.seller
                else None
            ),
            "buyer": (
                {
                    "id": self.buyer.id,
                    "name": f"{self.buyer.first_name} {self.buyer.last_name}",
                }
                if self.buyer
                else None
            ),
        }

from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum


class StatusType(str, Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    CANCELLED = 'cancelled'
    DELIVERED = 'delivered'
    RATED = 'rated'


class ItemTransaction(db.Model):
    __tablename__ = 'item_transactions'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(db.DateTime(
        timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(
        db.Numeric(10, 2), nullable=False)
    pickup_address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    delivery_address: Mapped[str] = mapped_column(
        db.String(255), nullable=False)
    delivery_status: Mapped[StatusType] = mapped_column(
        db.Enum(StatusType),
        nullable=False,
        default=StatusType.PENDING)
    rating: Mapped[int] = mapped_column(
        db.Integer, nullable=True, comment='Rating from buyer to seller (1-5)')

    # FK
    product_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # rel
    product = db.relationship('Product', backref='transactions')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    buyer = db.relationship('User', foreign_keys=[
                            buyer_id], backref='purchases')

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'quantity': self.quantity,
            'total_price': float(self.total_price),
            'pickup_address': self.pickup_address,
            'delivery_address': self.delivery_address,
            'delivery_status': self.delivery_status.value,
            'rating': self.rating if self.rating else None,
            'product': {
                'id': self.product.id,
                'name': self.product.name
            },
            'seller': {
                'id': self.seller.id,
                'name': f"{self.seller.first_name} {self.seller.last_name}"
            },
            'buyer': {
                'id': self.buyer.id,
                'name': f"{self.buyer.first_name} {self.buyer.last_name}"
            }
        }

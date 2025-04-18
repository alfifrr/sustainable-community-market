from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    SELL = 'sell'
    BUY = 'buy'


class TransactionHistory(db.Model):
    __tablename__ = 'transaction_history'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(db.Numeric(10, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(db.DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc))
    type: Mapped[TransactionType] = mapped_column(
        db.Enum(TransactionType), nullable=False)
    details = db.Column(db.JSON, nullable=True)

    # FK
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # rel
    user = db.relationship('User', back_populates='transaction_history')

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'date': self.date.isoformat(),
            'type': self.type.value,
            'details': self.details or {}
        }

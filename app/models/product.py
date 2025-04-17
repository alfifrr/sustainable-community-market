from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[int] = mapped_column(db.Integer, nullable=False)
    stock: Mapped[int] = mapped_column(db.Integer, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), nullable=False
    )
    product_posted: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    product_updated: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # FK
    pickup_address_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("addresses.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )

    # rel
    user = db.relationship("User", back_populates="products", lazy=True)
    category = db.relationship(
        "Category", back_populates="products", lazy=True)
    pickup_address = db.relationship(
        'Address', back_populates='products', lazy=True)

    def get_discounted_price(self) -> float:
        now = datetime.now(timezone.utc)
        exp = self.expiration_date.replace(tzinfo=timezone.utc)
        days_remaining = (self.expiration_date - now).days
        discount_map = {4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2, 0: 0.1}
        return float(self.price * discount_map[days_remaining])

    def __repr__(self):
        return f"<Product {self.name} from user {self.user_id}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "pickup_address": {
                "id": self.pickup_address_id,
                "label": self.pickup_address.label,
                'address': self.pickup_address.address,
                'contact_person': self.pickup_address.contact_person,
                'details': self.pickup_address.details
            },
            "expiration_date": self.expiration_date.isoformat(),
            "product_posted": self.product_posted.isoformat(),
            "product_updated": (
                self.product_updated.isoformat() if self.product_updated else None
            ),
            "category": {"id": self.category.id, "name": self.category.name},
            "user": {
                "id": self.user.id,
                "name": f"{self.user.first_name} {self.user.last_name}",
                "is_verified": self.user.is_verified,
            },
        }

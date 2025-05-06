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
    is_sustainable: Mapped[bool] = mapped_column(db.Boolean, default=False)
    sustainability_certifications = db.Column(db.JSON, default=list, nullable=False)
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
    category = db.relationship("Category", back_populates="products", lazy=True)
    pickup_address = db.relationship("Address", back_populates="products", lazy=True)

    def get_discounted_price(self) -> float:
        try:
            now = datetime.now(timezone.utc)
            exp_date = (
                self.expiration_date
                if self.expiration_date.tzinfo
                else self.expiration_date.replace(tzinfo=timezone.utc)
            )
            days_remaining = (exp_date - now).days
            if days_remaining < 0:
                return 0
            discount_map = {4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2, 0: 0.1}
            return float(self.price * discount_map[days_remaining])
        except Exception as e:
            return float(self.price)

    def calculate_total_discount(self, quantity: int) -> tuple[float, dict]:
        """Calculate final price after all discounts
        Returns tuple of (final_price, discount_details)"""
        base_price = self.price * quantity
        discounts = {}

        # Expiration date discount
        exp_discount = (1 - (self.get_discounted_price() / self.price)) * 100
        if exp_discount > 0:
            discounts["expiration"] = {
                "percentage": exp_discount,
                "amount": base_price * (exp_discount / 100),
            }

        # Bulk purchase discount (example: 5% off for 5+ items)
        bulk_discount = 0
        if quantity >= 5:
            bulk_discount = 5
            discounts["bulk"] = {
                "percentage": bulk_discount,
                "amount": base_price * (bulk_discount / 100),
            }

        # Calculate final price after all discounts
        total_discount_percentage = sum(
            d.get("percentage", 0) for d in discounts.values()
        )
        final_price = base_price * (1 - (total_discount_percentage / 100))

        return float(final_price), discounts

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
                "address": self.pickup_address.address,
                "contact_person": self.pickup_address.contact_person,
                "details": self.pickup_address.details,
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
            "is_sustainable": self.is_sustainable,
            "sustainability_certifications": self.sustainability_certifications,
        }

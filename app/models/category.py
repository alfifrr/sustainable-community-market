from app import db
from sqlalchemy.orm import Mapped, mapped_column


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        db.String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # rel
    products = db.relationship(
        'Product', back_populates='category', lazy='dynamic')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

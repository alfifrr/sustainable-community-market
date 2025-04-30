from app import db
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum


class RoleType(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"


class Role(db.Model):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[RoleType] = mapped_column(
        db.Enum(RoleType), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=True)

    # rel
    users = db.relationship('User', back_populates='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name.value,
            'description': self.description
        }

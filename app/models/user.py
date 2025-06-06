from secrets import token_urlsafe
from app import bcrypt, db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .role import RoleType, Role


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    balance: Mapped[float] = mapped_column(db.Numeric(10, 2), default=0.00)

    first_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(
        db.String(20), unique=True, nullable=False
    )

    date_joined: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    date_updated: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_activity: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), nullable=True
    )
    is_verified: Mapped[bool] = mapped_column(db.Boolean, default=False)

    activation_token: Mapped[str] = mapped_column(
        db.String(255), unique=True, nullable=True
    )

    role_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("roles.id"), nullable=True
    )

    # rel
    addresses = db.relationship("Address", back_populates="user", lazy="dynamic")
    products = db.relationship("Product", back_populates="user", lazy="dynamic")
    transaction_history = db.relationship(
        "TransactionHistory", back_populates="user", lazy="dynamic"
    )
    # sales = db.relationship("ItemTransaction", foreign_keys="ItemTransaction.seller_id")
    # purchases = db.relationship(
    #     "ItemTransaction", foreign_keys="ItemTransaction.buyer_id"
    # )
    role = db.relationship("Role", back_populates="users")

    def generate_activation_token(self):
        self.activation_token = token_urlsafe(32)
        return self.activation_token

    def activate_account(self):
        self.is_verified = True
        self.activation_token = None

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Add helper methods for RBAC
    def has_role(self, role: RoleType | str) -> bool:
        if isinstance(role, str):
            return self.role.name.value == role
        return self.role.name == role

    def is_admin(self) -> bool:
        return self.has_role(RoleType.ADMIN)

    def is_seller(self) -> bool:
        return self.has_role(RoleType.SELLER)

    def is_buyer(self) -> bool:
        return self.has_role(RoleType.BUYER)

    def is_expedition(self) -> bool:
        return self.has_role(RoleType.EXPEDITION)

    @classmethod
    def get_expeditions(cls, query: str = None):
        """Get all expedition users with optional name search"""
        base_query = cls.query.join(Role).filter(Role.name == RoleType.EXPEDITION)

        if query:
            return base_query.filter(
                db.or_(
                    db.func.lower(cls.first_name).like(f"%{query.lower()}%"),
                    db.func.lower(cls.last_name).like(f"%{query.lower()}%"),
                )
            ).all()
        return base_query.all()

    def __repr__(self):
        return f"<User {self.username}"

    def to_credentials(self):
        return {
            "id": self.id,
            "username": self.username,
            "balance": float(self.balance),
            "contact_info": {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
            },
            "date_joined": self.date_joined.isoformat(),
            "date_updated": (
                self.date_updated.isoformat() if self.date_updated else None
            ),
            "last_activity": (
                self.last_activity.isoformat() if self.last_activity else None
            ),
            "is_verified": self.is_verified,
            "role": self.role.name,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": f"{self.first_name} {self.last_name}",
            "date_joined": self.date_joined.isoformat(),
            "date_updated": (
                self.date_updated.isoformat() if self.date_updated else None
            ),
            "last_activity": (
                self.last_activity.isoformat() if self.last_activity else None
            ),
            "is_verified": self.is_verified,
            "role": self.role.name,
        }

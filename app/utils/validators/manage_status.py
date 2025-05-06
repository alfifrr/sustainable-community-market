from app.utils.validators.base import BaseForm
from wtforms import IntegerField, StringField
from wtforms.validators import (
    DataRequired,
    NumberRange,
    ValidationError,
    Optional,
    Length,
)
from flask_jwt_extended import get_jwt_identity
from app.models import ItemTransaction, StatusType, User


class ProcessForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID",
        validators=[DataRequired(message="Transaction ID is required")],
    )
    expedition_id = IntegerField(
        "Expedition ID",
        validators=[DataRequired(message="Expedition ID is required")],
    )

    def validate_expedition_id(self, field):
        expedition = User.query.get(field.data)
        if not expedition or not expedition.is_expedition():
            raise ValidationError("Invalid expedition user")

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            seller_id=current_user_id, id=field.data
        ).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.PENDING:
            raise ValidationError("Product already processed or cancelled")


class CancelForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID",
        validators=[DataRequired(message="Transaction ID is required")],
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            buyer_id=current_user_id, id=field.data
        ).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.PENDING:
            raise ValidationError("Product already processed or cancelled")


class ConfirmDeliveryForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID",
        validators=[DataRequired(message="Transaction ID is required")],
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Admin and expedition can confirm any delivery
        if current_user.is_admin():
            transaction = ItemTransaction.query.get(field.data)
        elif current_user.is_expedition():
            transaction = ItemTransaction.query.filter_by(
                id=field.data, assigned_expedition_id=current_user_id
            ).first()
        else:
            # Buyers can only confirm their own transactions
            transaction = ItemTransaction.query.filter_by(
                buyer_id=current_user_id, id=field.data
            ).first()

        if not transaction:
            raise ValidationError(
                "Transaction does not exist or you don't have permission to confirm it"
            )
        if transaction.delivery_status != StatusType.PROCESSED:
            raise ValidationError("Can only confirm processed product")


class RatingForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID",
        validators=[DataRequired(message="Transaction ID is required")],
    )
    rating = IntegerField(
        "Rating",
        validators=[
            DataRequired(message="Rating is required"),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5"),
        ],
    )
    testimonial = StringField(
        "Testimonial",
        validators=[
            Optional(),
            Length(max=1000, message="Testimonial must not exceed 1000 characters"),
        ],
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            buyer_id=current_user_id, id=field.data
        ).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.DELIVERED:
            raise ValidationError("Can only rate delivered product")
        if transaction.rating is not None:
            raise ValidationError("Product already rated")

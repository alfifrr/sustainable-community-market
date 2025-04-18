from app.utils.validators.base import BaseForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from flask_jwt_extended import get_jwt_identity
from app.models import ItemTransaction, StatusType


class ProcessForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID", validators=[DataRequired(message="Transaction ID is required")]
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            seller_id=current_user_id, id=field.data).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.PENDING:
            raise ValidationError('Product already processed or cancelled')


class CancelForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID", validators=[DataRequired(message="Transaction ID is required")]
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            buyer_id=current_user_id, id=field.data).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.PENDING:
            raise ValidationError('Product already processed or cancelled')


class ConfirmDeliveryForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID", validators=[DataRequired(message="Transaction ID is required")]
    )

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            buyer_id=current_user_id, id=field.data).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.PROCESSED:
            raise ValidationError('Can only confirm processed product')


class RatingForm(BaseForm):
    transaction_id = IntegerField(
        "Transaction ID", validators=[DataRequired(message="Transaction ID is required")]
    )
    rating = IntegerField('Rating', validators=[
        DataRequired(message='Rating is required'),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])

    def validate_transaction_id(self, field):
        current_user_id = get_jwt_identity()
        transaction = ItemTransaction.query.filter_by(
            buyer_id=current_user_id, id=field.data).first()
        if not transaction:
            raise ValidationError("Product listing does not exist")
        if transaction.delivery_status != StatusType.DELIVERED:
            raise ValidationError('Can only rate delivered product')
        if transaction.rating is not None:
            raise ValidationError('Product already rated')

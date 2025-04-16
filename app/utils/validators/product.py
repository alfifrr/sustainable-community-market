from app.utils.validators.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from app.models import Category, Address
from wtforms.fields import DateTimeField
from datetime import datetime, timezone
from flask_jwt_extended import get_jwt_identity


class ProductForm(BaseForm):
    name = StringField('Name', validators=[
        DataRequired(message='Product name is required'),
        Length(min=3, max=255,
               message='Product name must be between 3 and 255 characters')
    ])
    description = StringField('Description', validators=[
        DataRequired(message='Product description is required'),
        Length(min=10, max=255,
               message='Description must be between 10 and 255 characters')
    ])
    price = IntegerField('Price', validators=[
        DataRequired(message='Product price is required'),
        NumberRange(min=0, message='Price cannot be negative')
    ])
    stock = IntegerField('Stock', validators=[
        DataRequired(message='Product stock is required'),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    category_id = IntegerField('Category', validators=[
        DataRequired(message='Category ID is required')
    ])
    address_id = IntegerField('Address', validators=[
        DataRequired(message='Address ID is required')
    ])
    expiration_date = DateTimeField(
        'Expiration Date',
        validators=[
            DataRequired(message='Expiration date is required')
        ],
        format='%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 format

    def validate_category_id(self, field):
        category = Category.query.get(field.data)
        if not category:
            raise ValidationError('Category does not exist')

    def validate_address_id(self, field):
        current_user_id = get_jwt_identity()
        address = Address.query.filter_by(
            user_id=current_user_id,
            id=field.data).first()
        if not address:
            raise ValidationError('Address does not exist')

    def validate_expiration_date(self, field):
        expiration_date = field.data.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        if expiration_date <= current_time:
            raise ValidationError('Expiration date must be in the future')

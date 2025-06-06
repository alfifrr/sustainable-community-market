from app.utils.validators.base import BaseForm
from wtforms import StringField, IntegerField, FieldList
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    ValidationError,
    Optional,
)
from app.models import Category, Address, SustainabilityCertification
from wtforms.fields import DateTimeField
from datetime import datetime, timezone
from flask_jwt_extended import get_jwt_identity


class ProductForm(BaseForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Product name is required"),
            Length(
                min=3,
                max=255,
                message="Product name must be between 3 and 255 characters",
            ),
        ],
    )
    description = StringField(
        "Description",
        validators=[
            DataRequired(message="Product description is required"),
            Length(
                min=10,
                max=255,
                message="Description must be between 10 and 255 characters",
            ),
        ],
    )
    price = IntegerField(
        "Price",
        validators=[
            DataRequired(message="Product price is required"),
            NumberRange(min=1, message="Price cannot below zero"),
        ],
    )
    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="Product stock is required"),
            NumberRange(min=1, message="Stock cannot below zero"),
        ],
    )
    category_id = IntegerField(
        "Category", validators=[DataRequired(message="Category ID is required")]
    )
    address_id = IntegerField(
        "Address", validators=[DataRequired(message="Address ID is required")]
    )
    expiration_date = DateTimeField(
        "Expiration Date",
        validators=[
            DataRequired(
                message="Expiration date is required (example: 2026-11-22T23:59:59.359Z)"
            )
        ],
        format="%Y-%m-%dT%H:%M:%S.%fZ",
    )  # ISO 8601 format with milliseconds
    sustainability_certifications = FieldList(
        IntegerField("Certification ID"), validators=[Optional()]
    )

    def validate_category_id(self, field):
        category = Category.query.get(field.data)
        if not category:
            raise ValidationError("Category does not exist")

    def validate_address_id(self, field):
        current_user_id = get_jwt_identity()
        address = Address.query.filter_by(
            user_id=current_user_id, id=field.data
        ).first()
        if not address:
            raise ValidationError("Address does not exist")

    def validate_expiration_date(self, field):
        expiration_date = field.data.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        if expiration_date <= current_time:
            raise ValidationError("Expiration date must be in the future")

    def validate_sustainability_certifications(self, field):
        if field.data and len(field.data) > 0:
            for cert_id in field.data:
                cert = SustainabilityCertification.query.get(cert_id)
                if not cert:
                    raise ValidationError(
                        f"Certification with ID {cert_id} does not exist"
                    )

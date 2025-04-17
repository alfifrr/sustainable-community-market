from app.utils.validators.base import BaseForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from flask_jwt_extended import get_jwt_identity
from app.models import Address, Product


class BuyProductForm(BaseForm):
    product_id = IntegerField(
        "Product ID", validators=[DataRequired(message="Product ID is required")]
    )
    quantity = IntegerField(
        "Quantity",
        validators=[
            DataRequired(message="Quantity is required"),
            NumberRange(min=1, message="Quantity cannot below zero"),
        ],
    )
    address_id = IntegerField(
        "Address ID", validators=[DataRequired(message="Address ID is required")]
    )

    def validate_product_id(self, field):
        product = Product.query.get(field.data)
        if not product:
            raise ValidationError("Product does not exist")
        self._product = product

    def validate_quantity(self, field):
        if hasattr(self, "_product"):
            if self._product.stock < field.data:
                raise ValidationError("Quantity exceeds product stock")

    def validate_address_id(self, field):
        current_user_id = get_jwt_identity()
        address = Address.query.filter_by(
            user_id=current_user_id, id=field.data
        ).first()
        if not address:
            raise ValidationError("Address does not exist")

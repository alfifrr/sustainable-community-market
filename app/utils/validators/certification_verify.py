from app.utils.validators.base import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError


class CertificationVerifyForm(BaseForm):
    status = StringField(
        "Status",
        validators=[DataRequired(message="Status is required")],
    )

    def validate_status(self, field):
        allowed_values = ["approved", "rejected"]
        if field.data.lower() not in allowed_values:
            raise ValidationError("Status must be either 'approved' or 'rejected'")

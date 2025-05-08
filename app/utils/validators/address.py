from app.utils.validators.base import BaseForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class AddressForm(BaseForm):
    label = StringField('label', validators=[
        DataRequired(message='Label is required'),
        Length(min=3, max=50, message='Label must be between 3 and 50 characters')
    ])
    address = StringField('address', validators=[
        DataRequired(message='Address is required'),
        Length(min=5, max=255, message='Address must be between 5 and 255 characters')
    ])
    details = StringField('details', validators=[
        Length(max=255, message='Details must not exceed 255 characters')
    ])
    contact_person = StringField('contact_person', validators=[
        DataRequired(message='Contact person is required'),
        Length(
            min=3,
            max=255,
            message='Contact person must be between 3 and 255 characters'
        )
    ])
    latitude = FloatField('latitude', validators=[
        Optional(),
        NumberRange(min=-90, max=90,
                    message='Latitude must be between -90 and 90 degrees')
    ])
    longitude = FloatField('longitude', validators=[
        Optional(),
        NumberRange(min=-180, max=180,
                    message='Longitude must be between -180 and 180 degrees')
    ])

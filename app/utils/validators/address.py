from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class AddressForm(FlaskForm):
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

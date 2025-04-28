from app.utils.validators.base import BaseForm
from wtforms import StringField, PasswordField
from wtforms.validators import (
    Length,
    InputRequired,
    Regexp, ValidationError
)
from app.models import User


class ProfileUpdateForm(BaseForm):
    username = StringField('username', validators=[
        InputRequired(message="Username is required"),
        Length(min=6, message="Username must be at least 6 characters long"),
        Regexp(
            r'^[a-z0-9]+$', message="Username can only contain lowercase letters and numbers")
    ])

    old_password = PasswordField('old_password', validators=[
        InputRequired(message="Current password is required")
    ])

    password = PasswordField('password', validators=[
        InputRequired(message="New password is required"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[^\s]+$',
               message="Password must contain 1 uppercase, 1 number, and 1 symbol")
    ])

    first_name = StringField('first_name', validators=[
        InputRequired(message="First name is required"),
        Length(min=3, message="First name must be at least 3 characters long"),
        Regexp(r'^[a-zA-Z]+$', message="First name can only contain letters")
    ])

    last_name = StringField('last_name', validators=[
        InputRequired(message="Last name is required"),
        Length(min=3, message="Last name must be at least 3 characters long"),
        Regexp(r'^[a-zA-Z]+$', message="Last name can only contain letters")
    ])

    phone_number = StringField('phone_number', validators=[
        InputRequired(message="Phone number is required"),
        Length(min=10, message="Phone number must be at least 10 digits long"),
        Regexp(r'^\d+$', message="Phone number can only contain digits")
    ])

    def validate_old_password(self, field):
        user = User.query.get(self.user_id)
        if not user or not user.check_password(field.data):
            raise ValidationError('Current password is incorrect')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and str(user.id) != str(self.user_id):
            raise ValidationError('Username already exists')

    def validate_phone_number(self, field):
        user = User.query.filter_by(phone_number=field.data).first()
        if user and str(user.id) != str(self.user_id):
            raise ValidationError('Phone number already exists')

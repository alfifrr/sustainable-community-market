from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (
    Email, Length,
    InputRequired,
    Regexp
)


class SignupForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(message="Username is required"),
        Length(min=6, message="Username must be at least 6 characters long"),
        Regexp(
            r'^[a-z0-9]+$', message="Username can only contain lowercase letters and numbers")
    ])

    password = PasswordField('password', validators=[
        InputRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[^\s]+$',
               message="Password must contain 1 uppercase, 1 number, and 1 symbol")
    ])

    email = StringField('email', validators=[
        InputRequired(message="Email is required"),
        Email(message="Invalid email address")
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

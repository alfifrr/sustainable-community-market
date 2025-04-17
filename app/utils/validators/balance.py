from app.utils.validators.base import BaseForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class DepositForm(BaseForm):
    amount = IntegerField(
        'Amount',
        validators=[
            DataRequired(message='Deposit amount is required'),
            NumberRange(min=0, message='Deposit amount cannot be negative')
        ]
    )


class WithdrawalForm(BaseForm):
    amount = IntegerField(
        'Amount',
        validators=[
            DataRequired(message='Withdrawal amount is required'),
            NumberRange(min=0, message='Withdrawal amount cannot be negative')
        ]
    )

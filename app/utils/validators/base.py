from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_validation_error(self):
        return {
            'status': 'error',
            'error': 'Validation error',
            'message': self.errors
        }

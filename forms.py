import wtforms
from wtforms import validators


class LoginForm(wtforms.Form):
    email = wtforms.StringField('Email', validators=[validators.DataRequired()])
    password = wtforms.PasswordField('Password',  validators=[validators.DataRequired()])

    def validate(self, *args, **kwargs):
        from models import User
        if not super(LoginForm, self).validate():
            return False
        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append('Invalid email or password')
            return False
        return True

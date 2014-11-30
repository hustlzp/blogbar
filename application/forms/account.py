# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from ..models import User


class SigninForm(Form):
    """Form for signin"""
    email = StringField('邮箱',
                        validators=[
                            DataRequired(),
                            Email()
                        ],
                        description='Email')

    password = PasswordField('密码',
                             validators=[DataRequired()],
                             description='Password')

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if not user:
            raise ValueError("Account doesn't exist.")

    def validate_password(self, field):
        if self.email.data:
            user = User.query.filter(User.email == self.email.data,
                                     User.password == self.password.data).first()
            if not user:
                raise ValueError('Password cannot match the Email.')
            else:
                self.user = user
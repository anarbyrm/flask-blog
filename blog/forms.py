from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password  = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm password', validators=[EqualTo('password_confirm', message='Two passwords needs to be the same.')])


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password  = PasswordField('Password', validators=[DataRequired()])

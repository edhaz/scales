from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Regsiter')

    def validate_username(self, username):
        user_name = User.query.filter_by(username=username.data).first()
        if user_name is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email is not None:
            raise ValidationError('Please use a different email address.')

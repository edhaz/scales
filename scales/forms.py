from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from . import store


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password")])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Regsiter")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password must be 8 or more characters")

    def validate_username(self, username):
        if store.get_user_by_name(username.name) is not None:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        if store.get_user_by_email(email.data) is not None:
            raise ValidationError("Email address already in use")

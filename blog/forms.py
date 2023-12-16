from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp, ValidationError
from blog.models import User
from sqlalchemy import func


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(), Email(), EqualTo('email')])
    
    # Custom password validator for enforcing at least one capital letter and special character
    password_validator = [
        DataRequired(),
        Length(min=7, max=15),
        Regexp(
            regex=r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:;<>,.?/~]).+$',
            message="Password must contain at least one capital letter and one special character."
        )
    ]

    password = PasswordField('Password', validators=password_validator)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=15), EqualTo('password')])
    submit = SubmitField('Sign Up.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, try another username')
        else:
            return f'This username is all yours!'
        
    def validate_email(self, email):
        user = User.query.filter_by(email=func.lower(email.data)).first()
        if user:
            raise ValidationError('That email is taken, try another email')


# A class for the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

from flask import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, FileAllowed, EqualTo, Email
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

#Update user information
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update.')
    picture = FileField('Update your profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user.username.data != current_user.username:
            if user:
                raise ValidationError('Wowza, that username is taken, try another username')
            else:
                return f'{user.username.data} is available for you!'
    
    def validate_user(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user.email.data != current_user.username:
            if user:
                raise ValidationError('Wowza, that email is taken, try another email')

# To request for a new password
class RequestPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password')

    def validate_email(self, email):
        user = User.query.filter_by(email=func.lower(email.data)).first()
        if user:
            raise ValidationError('Wowza, there is no account registered under that email!')
        
# To update new password
class ResetPasswordForm(FlaskForm):
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
    submit = SubmitField('Reset password')
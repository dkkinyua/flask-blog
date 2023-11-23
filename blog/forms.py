from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(), Email(), EqualTo('email')])
    
    # Custom password validator for enforcing at least one capital letter and special character
    password_validator = [
        DataRequired(),
        Length(min=8, max=15),
        Regexp(
            regex=r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:;<>,.?/~]).+$',
            message="Password must contain at least one capital letter and one special character."
        )
    ]

    password = PasswordField('Password', validators=password_validator)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=15), EqualTo('password')])
    submit = SubmitField('Sign Up.')


# A class for the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

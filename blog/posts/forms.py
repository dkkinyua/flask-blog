from flask import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# To create a new post
class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = TextAreaField("Content Here", validators=[DataRequired()])
    submit = SubmitField('Post')
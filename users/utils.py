import os
import secrets
from flask import url_for
from flask_mail import Message
from PIL import Image
from blog import mail, app
from blog.models import User


# A function that saves the profile picture uploaded by the user
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext= os.path.splitext(form_picture.filename) #Splits the filename and filetype i.e. 'jpg', 'png'
    picture_fn = random_hex + f_ext # Adds the random_hex created above and the file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resizing the selected picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# a function to send reset emails to the user
def send_reset_email(user):
    user = User()
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='no-reply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, please follow the link: {url_for('users.reset_token', token=token, _external=True)}
If you did not request for a password change, please ignore this mail as no changes will be made to your profile.
This message has been sent by admin.
'''
    mail.send(msg)
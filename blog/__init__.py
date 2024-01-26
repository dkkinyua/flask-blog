# This file is a file to initialize our web app, contains initialization code
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime as datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = b'ea8d0505b73e07a44a3bbd4a24392a45' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from blog.users.routes import users
from blog.posts.routes import posts
from blog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
# All our configuration variables are here!
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY').encode('utf-8')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

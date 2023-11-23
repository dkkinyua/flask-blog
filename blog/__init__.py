from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime as datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea8d0505b73e07a44a3bbd4a24392a45' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from blog import routes
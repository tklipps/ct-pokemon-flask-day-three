from flask import Flask
from config import Config 
from flask_login import LoginManager #to log users in and out and maintain the session
from flask_sqlalchemy import SQLAlchemy #this talk to the database
from flask_migrate import Migrate #this makes altering the db a lot easier

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import routes
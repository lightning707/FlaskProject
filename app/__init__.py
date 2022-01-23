from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app_flask = Flask(__name__)
app_flask.config.from_object(Config)

db = SQLAlchemy(app_flask)

migrate = Migrate(app_flask, db)

login = LoginManager(app_flask)
login.login_view = 'login'


from app import routes, models

from flask import Flask
from config import Config

app_flask = Flask(__name__)
app_flask.config.from_object(Config)

from app import routes

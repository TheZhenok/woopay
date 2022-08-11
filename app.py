from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_httpauth import HTTPBasicAuth

from config import Config


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
auth: HTTPBasicAuth = HTTPBasicAuth()
db: SQLAlchemy = SQLAlchemy(app)
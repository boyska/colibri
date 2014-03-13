from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask_bootstrap import Bootstrap
from config import basedir

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config.from_object('config')
db = SQLAlchemy(app)
api_manager = APIManager(app, flask_sqlalchemy_db=db)
Bootstrap(app)

from app import models
db.create_all()
from app import api, auth, views, admin


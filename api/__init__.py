from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object('config')
#app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from .views import curso_views
from .models import curso_model





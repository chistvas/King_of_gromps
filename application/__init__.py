from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = '395f645c16a60709237dd22e9845ec41'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from application import routes
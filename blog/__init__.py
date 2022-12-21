from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

from blog.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id=id)
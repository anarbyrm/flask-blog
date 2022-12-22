from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e@8j96=#n_jmv92xo)qz0)n4jp3_)4th=_4&g8%96p)+dz_al@'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.de = True
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

from blog.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_first_request
def create_tables():
    db.create_all()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nikhil-varma"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    from .auth import auth
    from .views import views
    app.register_blueprint(views)
    app.register_blueprint(auth)
    manage = LoginManager()
    manage.login_view = "auth.login"
    manage.init_app(app)
    from .models import User

    @manage.user_loader
    def loader(ids):
        return User.query.get(int(ids))

    if not path.exists("website/users.db"):
        db.create_all(app=app)
    return app

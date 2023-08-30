from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_bcrypt import Bcrypt

from main.config import Config






db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Auth.login' # type: ignore
login_manager.login_message_category = 'info'





def create_app(config_class = Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)


    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)


    from main.Auth.routes import auth
    from main.Posts.routes import posts
    from main.Home.routes import mainHome


    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(mainHome)


    return app
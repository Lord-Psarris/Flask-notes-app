from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jdgalwbeflahugfs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # tells the app which db to use

    # this tells the flask app to init this db with this app
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,
                           url_prefix='/')  # the url-prefix is for the prefix of each url e.g /views/<actual url>
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, User  # getting the dbs
    create_database(app)

    # to tell flask which login manager to use

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created db')

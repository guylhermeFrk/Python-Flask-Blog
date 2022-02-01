from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():  # Cria uma aplicação flask e a retorna.
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views  # importando view
    from .auth import auth  # importando auth

    app.register_blueprint(views, url_prefix='/')  # registrando view com o app
    app.register_blueprint(auth, url_prefix='/auth')  # registrando auth com o app

    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Se alguém tentar acessar alguma página sem estar logado, será redirecionado para auth.login
    login_manager.login_message = 'Por favor, faça o login para acessar esta página.' #  Adicionei por conta própria.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")

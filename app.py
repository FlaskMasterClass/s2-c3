import os

import click
import flask
from flask import Flask
from flask import current_app
from flask import redirect
from flask import render_template
from flask.cli import load_dotenv
from flask_login import AnonymousUserMixin
from flask_login import UserMixin

from auth_views import auth_blueprint
from secret_views import secret_blueprint
from init import db
from init import login_manager
from init import migrate
from models import User


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


from config import DevelopmentConfig
from config import ProductionConfig
from config import TestingConfig

profiles = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig()
}

def create_app(profile):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(profiles[profile])
    app.config.from_pyfile("config.py", silent=True)


    app.register_blueprint(auth_blueprint)
    app.register_blueprint(secret_blueprint)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    if profile != "testing":
        app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.shell_context_processor
    def shell():
        return {
            "db": db,
            "User": User
        }

    # inlining route
    @app.route('/')
    def home():
        # --- demo purposes --
        try:
            db.create_all()
        except:
            pass 

        try:
            u = User(email='admin@domain.com')
            u.password = 'pass'
            db.session.add(u)
            db.session.commit()
        except: 
            pass
        return render_template('home.html')
        # ---
        
    return app


flask_env = os.environ.get("FLASK_ENV", default="development")
app = create_app(flask_env)


# -*- coding: utf-8 -*-
import os

from flask import Flask

from app.controllers import auth, public
from app.extension import cors, csrf, db
from Models.base import Model

from .config import config


def create_app(config_name=os.environ.get("FLASK_ENV")):
    """App factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    register_context_callbacks(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_context_callbacks(app: Flask):
    @app.before_request
    def set_model_session():
        Model.set_session(db.session)

    @app.teardown_appcontext
    def unset_model_session(response_or_exc):
        Model.set_session(None)
        return response_or_exc


def register_extensions(app: Flask):
    """Register Flask extensions."""
    # login_manager.init_app(app)
    # oauth.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    # session.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.blueprint)
    app.register_blueprint(auth.blueprint)

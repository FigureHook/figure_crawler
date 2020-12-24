# -*- coding: utf-8 -*-
import os

from flask import Flask

from app.controllers import auth, public
from app.extension import cors, csrf

from .config import config


def create_app(config_name=os.environ.get("FLASK_ENV")):
    """App factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    # login_manager.init_app(app)
    # oauth.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.blueprint)
    app.register_blueprint(auth.blueprint)
    return None

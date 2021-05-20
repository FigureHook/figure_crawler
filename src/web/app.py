# -*- coding: utf-8 -*-
from web.utils import get_maintenance_time
import os
from distutils.util import strtobool

from flask import Flask, request
from flask.helpers import make_response
from flask.templating import render_template
from flask_babel import get_locale

from Models.base import Model
from web.controllers import auth, public
from web.extension import babel, cors, csrf, db, session

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
    def check_maintenance():
        maintenance_flag = request.headers.get('X-In-Maintenance', '0')
        is_in_maintenance = strtobool(maintenance_flag)  # type: ignore
        if is_in_maintenance:
            retry_after = get_maintenance_time()
            response = make_response(
                render_template(
                    '503.html',
                    lang=str(get_locale())
                ), 503)

            response.headers['Retry-After'] = retry_after
            return response

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
    session.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['en', 'ja', 'zh'], default='en')


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.blueprint)
    app.register_blueprint(auth.blueprint)

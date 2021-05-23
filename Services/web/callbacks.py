from distutils.util import strtobool

from figure_hook.Models.base import Model
from flask import request, abort
from flask.helpers import make_response
from flask.templating import render_template
from flask_babel import get_locale

from .extension import db

__all__ = [
    "check_maintenance",
    "set_model_session",
    "unset_model_session"
]


def get_maintenance_time():
    try:
        with open('/flags/maintenance.on', 'r') as f:
            retry_after = f.readline().strip()
        return retry_after
    except FileNotFoundError:
        return '3600'


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
        abort(response)


def set_model_session():
    Model.set_session(db.session)


def unset_model_session(response_or_exc):
    Model.set_session(None)
    return response_or_exc

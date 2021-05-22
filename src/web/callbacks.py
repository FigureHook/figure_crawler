
from distutils.util import strtobool

from flask import request
from flask.helpers import make_response
from flask.templating import render_template
from flask_babel import get_locale

from Models.base import Model
from web.extension import db
from web.utils import get_maintenance_time


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


def set_model_session():
    Model.set_session(db.session)


def unset_model_session(response_or_exc):
    Model.set_session(None)
    return response_or_exc

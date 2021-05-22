# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from authlib.integrations.flask_client import OAuth
from flask_babel import Babel
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

session = Session()
login_manager = LoginManager()
oauth = OAuth()
cors = CORS()
csrf = CSRFProtect()
db = SQLAlchemy()
babel = Babel()

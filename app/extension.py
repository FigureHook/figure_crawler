# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
oauth = OAuth()
cors = CORS()
csrf = CSRFProtect()
db = SQLAlchemy()

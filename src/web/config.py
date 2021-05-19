import os
from base64 import b64encode
from os import urandom
import redis


class Config(object):
    """Base config, uses staging database server."""
    DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = True
    SESSION_REDIS = redis.from_url(f"redis://{os.environ.get('REDIS_URL')}")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.getenv("DB_URL")
        return f"postgresql+psycopg2://{db_url}"


class ProductionConfig(Config):
    """Uses production database server."""
    SERVER_NAME = os.environ.get("FLASK_SERVER_NAME")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = 3600


class DevelopmentConfig(Config):
    # SERVER_NAME = "127.0.0.1:5000"
    CORS_ORIGINS = "*"
    SECRET_KEY = b64encode(urandom(32)).decode('utf-8')
    SESSION_PERMANENT = False


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.getenv("TEST_DB_URL")
        return f"postgresql+psycopg2://{db_url}"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig
}

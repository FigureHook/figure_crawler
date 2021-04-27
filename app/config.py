import os

db_url = os.getenv("DB_URL")


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(32)
    DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # @property
    # def REMEMBER_COOKIE_DOMAIN(self):
    #     return f".{self.SERVER_NAME}"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.getenv("DB_URL")
        return f"postgresql+psycopg2://{db_url}"


class ProductionConfig(Config):
    """Uses production database server."""


class DevelopmentConfig(Config):
    # SERVER_NAME = "127.0.0.1:5000"
    CORS_ORIGINS = "*"
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig
}

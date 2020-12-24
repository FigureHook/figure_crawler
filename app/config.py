import os


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(32)
    DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")

    @property
    def REMEMBER_COOKIE_DOMAIN(self):
        return f".{self.SERVER_NAME}"
    # @property
    # def DATABASE_URI(self):         # Note: all caps
    #     return "mysql://user@{}/foo".format(self.DB_SERVER)


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

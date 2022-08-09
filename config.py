import os


class Config:
    TESTING = False
    ENV_VAR = os.environ.get("ENV_VAR")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True

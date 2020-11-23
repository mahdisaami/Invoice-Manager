import os
from local_settings import DATABASE_URI, SECRET_KEY, DEBUG


class Config:
    REDIS_URL = 'redis://localhost:6379/1'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = DEBUG
    # FLASK_ADMIN_SWATCH = 'cerulean'
    SECRET_KEY = SECRET_KEY
    STATIC_DIR = 'static'

from flask_mongoengine import MongoEngine

from . import users
from . import oauth2

from .users import User

db = MongoEngine()


def init_db(app):
    db.init_app(app)

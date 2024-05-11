import pathlib
from flask_mongoengine import MongoEngine

import importlib
import logging

logger = logging.getLogger(__name__)

db = MongoEngine()


def regist_models(directory):
    for module in directory.iterdir():
        model_file = module / "models.py"

        if not model_file.exists():
            continue

        package = module.parts[len(pathlib.Path.cwd().parts) :]
        try:
            pymod_file = f"{'.'.join(package)}.{model_file.stem}"
            pymod = importlib.import_module(pymod_file)
            print("regit model:", pymod)
        except Exception as e:
            logger.exception(e)


def init_db(app):
    module_directory = pathlib.Path(__file__).parent.parent / "web" / "modules"
    regist_models(module_directory)

    from . import oauth2

    db.init_app(app)

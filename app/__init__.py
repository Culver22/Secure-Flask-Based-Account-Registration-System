from flask import Flask
from config import Config
import logging
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.Formatter.converter = time.gmtime # UTC clock
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    from .routes import main
    app.register_blueprint(main)
    return app
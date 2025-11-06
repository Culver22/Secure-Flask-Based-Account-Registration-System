from flask import Flask
from config import Config
import logging
import time
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # logging output format
    handler = logging.StreamHandler() # for returning logs in terminal
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.Formatter.converter = time.gmtime # using UTC clock for logs
    handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)

    # only add handler once, don't attach a duplicate if flask reloads
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.register_blueprint(main)
    return app
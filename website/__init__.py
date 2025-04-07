from flask import Flask
import json

app = Flask(__name__)


def create_app():
    from .home import home

    app.register_blueprint(home, url_prefix="/")

    return app

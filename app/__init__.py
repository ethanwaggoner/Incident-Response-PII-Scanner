from flask import Flask, url_for, redirect
from importlib import import_module
import os


def register_blueprints(app):
    module = import_module('app.dashboard.routes')
    app.register_blueprint(module.blueprint)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(32)
    register_blueprints(app)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard_bp.dashboard'))

    return app

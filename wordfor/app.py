# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError

from wordfor import public
from wordfor.api.errors import APIError
from wordfor.api.v1 import users
from wordfor.api.v1 import search
from wordfor.api.v1 import words
from wordfor.assets import assets
from wordfor.extensions import (bcrypt, cache, db, debug_toolbar,
                                login_manager, migrate)
from wordfor.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(search.views.blueprint)
    app.register_blueprint(words.views.blueprint)
    return None


def register_error_handlers(app):
    """Register the error handlers we want to use."""
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(ex):
        response = jsonify(message="422: Unprocessable Entity",
                           description=ex.messages)
        response.status_code = 422
        return response

    @app.errorhandler(APIError)
    def handle_api_error(ex):
        response = jsonify(message=ex.message, description=ex.description)
        response.status_code = ex.status_code
        return response

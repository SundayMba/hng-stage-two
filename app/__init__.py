from flask import Flask, jsonify
from config import config
from .api import api as api_blueprint
from .auth import auth as auth_blueprint
from .extensions import db, jwt

def create_app(env: str):
    """
        flask app factory function.
    
    Keyword arguments:
    env -- the environment flask is running on. e.g Developement, Production
           Testing environment.
    Return: None
    """
    app = Flask(__name__)
    app.config.from_object(config[env])
    config[env].init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    """Initialize blueprint"""
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 401,
            'message': 'The token has expired'
        }), 401

    return app
    
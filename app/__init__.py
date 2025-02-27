from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from .routes.history import history_bp
    app.register_blueprint(history_bp, url_prefix='/api/history')

    return app
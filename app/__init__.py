from flask import Flask
from flask_cors import CORS
from .config import Config

app = Flask(__name__)

def create_app():
    CORS(app)
    app.config.from_object(Config)

    from .routes.history import history_bp
    app.register_blueprint(history_bp, url_prefix='/api/history')

    return app
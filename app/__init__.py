import os
from flask import Flask
from .views import main_bp
from .admin import admin_bp
from .config_store import ConfigStore


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # Initialize config store
    app.config_store = ConfigStore(os.environ.get("CONFIG_PATH", "/workspace/config.json"))

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    return app

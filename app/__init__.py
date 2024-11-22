from flask import Flask
from .routes import api

def create_app():
    """Crear y configurar la aplicación Flask"""
    app = Flask(__name__)

    # Registrar el Blueprint
    app.register_blueprint(api)

    return app
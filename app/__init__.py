from flask import Flask
from flask_cors import CORS
from .routes import api

def create_app():
    """Crear y configurar la aplicación Flask"""
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

    # Habilitar CORS
    CORS(app)

    # Registrar el Blueprint
    app.register_blueprint(api)

    return app
from flask import Flask
from flask_cors import CORS
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

    CORS(app)

    app.register_blueprint(api)

    return app
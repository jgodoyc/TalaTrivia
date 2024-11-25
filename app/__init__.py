from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import api
import os

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

    CORS(app)

    app.register_blueprint(api)
    
    SWAGGER_URL = '/swagger'
    API_URL = '/openapi.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "TalaTrivia API"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route('/openapi.yaml')
    def serve_openapi():
        return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'openapi.yaml')

    return app
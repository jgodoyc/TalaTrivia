from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from .routes.auth_routes import api as auth_ns
from .routes.user_routes import api as user_ns
from .routes.trivia_routes import api as trivia_ns
from .routes.question_routes import api as question_ns
from .routes.option_routes import api as option_ns
from .routes.answer_routes import api as answer_ns

def create_app():
    app = Flask(__name__)
    CORS(app)

    api = Api(app, version='1.0', title='TalaTrivia API',
             description='API para el juego TalaTrivia')

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(trivia_ns, path='/trivias')
    api.add_namespace(question_ns, path='/questions')
    api.add_namespace(option_ns, path='/options')
    api.add_namespace(answer_ns, path='/answers')

    return app
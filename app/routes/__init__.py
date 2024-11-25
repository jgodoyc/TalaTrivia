from flask import Blueprint

api = Blueprint('api', __name__)

from .login import login_bp
from .users import users_bp
from .questions import questions_bp
from .options import options_bp
from .trivias import trivias_bp

api.register_blueprint(login_bp)
api.register_blueprint(users_bp)
api.register_blueprint(questions_bp)
api.register_blueprint(options_bp)
api.register_blueprint(trivias_bp)
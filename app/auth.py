import jwt
import os
import datetime
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
from .services.user_services import get_user_by_id

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now(datetime.UTC),
        'sub': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['sub']
            user = get_user_by_id(user_id)
            if user['role'] != 'admin':
                return jsonify({"error": "Admin access required!"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 403
        
        return f(*args, **kwargs)
    return decorated_function


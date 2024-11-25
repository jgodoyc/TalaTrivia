from flask import Blueprint, jsonify, request
from ..auth import generate_token
from ..db import connection as get_connection

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email y contraseña son requeridos'}), 400
    
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, email, role FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
        connection.close()
        
        if user:
            token = generate_token(user['id']) 
            return jsonify({'token': token, 'userId': user['id'], 'role': user['role']}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
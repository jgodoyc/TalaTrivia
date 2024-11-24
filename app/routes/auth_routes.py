from flask import request, jsonify
from flask_restx import Namespace, Resource
from ..auth import generate_token
from ..db import connection as get_connection

api = Namespace('auth', description='Operaciones de autenticación')

@api.route("/login")
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
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
                return jsonify({'message': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
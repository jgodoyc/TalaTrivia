from flask import jsonify, request
from flask_restx import Namespace, Resource
from ..services.user_services import (
    get_all_users, create_new_user, get_user_by_id, update_user_by_id, delete_user_by_id
)
from ..auth import token_required, admin_required

api = Namespace('users', description='Operaciones relacionadas con usuarios')

@api.route("/")
class UserList(Resource):
    @token_required
    def get(self, current_user):
        try:
            result = get_all_users()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @token_required
    def post(self, current_user):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        role = data.get('role', 'jugador')
        try:
            create_new_user(name, email, role)
            return jsonify({"message": "Usuario creado exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:user_id>")
class User(Resource):
    @token_required
    def get(self, current_user, user_id):
        try:
            user = get_user_by_id(user_id)
            return jsonify(user)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @token_required
    def put(self, current_user, user_id):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')
        try:
            update_user_by_id(user_id, name, email, role)
            return jsonify({"message": "Usuario actualizado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @token_required
    def delete(self, current_user, user_id):
        try:
            delete_user_by_id(user_id)
            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
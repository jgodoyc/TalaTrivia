from flask import Blueprint, jsonify, request
from ..auth import token_required
from ..services.user_service import (
    get_all_users, create_new_user, get_user_by_id, update_user_by_id, delete_user_by_id
)

users_bp = Blueprint('users', __name__)

@users_bp.route("/users", methods=["GET"])
@token_required
def list_users(current_user):
    try:
        result = get_all_users()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users", methods=["POST"])
@token_required
def create_user(current_user):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'jugador')
    
    if not name or not email or not password:
        return jsonify({"message": "Nombre, email y contraseña son requeridos"}), 400
    
    try:
        create_new_user(name, email, password, role)
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(current_user, user_id):
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@token_required
def update_user(current_user, user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not name or not email or not password:
        return jsonify({"message": "Nombre, email y contraseña son requeridos"}), 400
    
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        update_user_by_id(user_id, name, password, email, role)
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, user_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        delete_user_by_id(user_id)
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
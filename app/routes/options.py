from flask import Blueprint, jsonify, request
from ..auth import admin_required
from ..services.option_service import (delete_option_by_id, get_option_by_id, update_option_by_id)

options_bp = Blueprint('options', __name__)

@options_bp.route("/options/<int:option_id>", methods=["GET"])
def get_option(option_id):
    try:
        option = get_option_by_id(option_id)
        
        if not option:
            return jsonify({"message": "Opción no encontrada"}), 404
        
        return jsonify(option)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@options_bp.route("/options/<int:option_id>", methods=["PUT"])
@admin_required
def update_option(option_id):
    data = request.get_json()
    option_text = data.get('option_text')
    is_correct = data.get('is_correct')
    
    if not option_text or is_correct is None:
        return jsonify({"message": "Texto de la opción y si es correcta son requeridos"}), 400
    
    try:
        option = get_option_by_id(option_id)
        if not option:
            return jsonify({"message": "Opción no encontrada"}), 404
        
        update_option_by_id(option_id, option_text, is_correct)
        return jsonify({"message": "Opción actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@options_bp.route("/options/<int:option_id>", methods=["DELETE"])
@admin_required
def delete_option(option_id):
    try:
        option = get_option_by_id(option_id)
        if not option:
            return jsonify({"message": "Opción no encontrada"}), 404
        
        delete_option_by_id(option_id)
        return jsonify({"message": "Opción eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
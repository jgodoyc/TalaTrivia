from flask import jsonify, request
from flask_restx import Namespace, Resource
from ..services.option_services import (
    get_option_by_id, update_option_by_id, delete_option_by_id
)
from ..auth import admin_required

api = Namespace('options', description='Operaciones relacionadas con opciones')

@api.route("/<int:option_id>")
class Option(Resource):
    def get(self, option_id):
        try:
            option = get_option_by_id(option_id)
            return jsonify(option)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def put(self, option_id):
        data = request.get_json()
        option_text = data.get('option_text')
        is_correct = data.get('is_correct')
        try:
            update_option_by_id(option_id, option_text, is_correct)
            return jsonify({"message": "Opción actualizada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def delete(self, option_id):
        try:
            delete_option_by_id(option_id)
            return jsonify({"message": "Opción eliminada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
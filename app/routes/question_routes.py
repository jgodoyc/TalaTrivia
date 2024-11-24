from flask import jsonify, request
from flask_restx import Namespace, Resource
from ..services.question_services import (
    get_all_questions, create_new_question, get_question_by_id, update_question_by_id, delete_question_by_id
)
from ..auth import token_required, admin_required

api = Namespace('questions', description='Operaciones relacionadas con preguntas')

@api.route("/")
class QuestionList(Resource):
    def get(self):
        try:
            result = get_all_questions()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def post(self):
        data = request.get_json()
        question = data.get('question')
        difficulty = data.get('difficulty')
        options = data.get('options')
        try:
            create_new_question(question, difficulty, options)
            return jsonify({"message": "Pregunta creada exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:question_id>")
class Question(Resource):
    def get(self, question_id):
        try:
            question = get_question_by_id(question_id)
            return jsonify(question)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def put(self, question_id):
        data = request.get_json()
        question = data.get('question')
        difficulty = data.get('difficulty')
        options = data.get('options')
        try:
            update_question_by_id(question_id, question, difficulty, options)
            return jsonify({"message": "Pregunta actualizada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def delete(self, question_id):
        try:
            delete_question_by_id(question_id)
            return jsonify({"message": "Pregunta eliminada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
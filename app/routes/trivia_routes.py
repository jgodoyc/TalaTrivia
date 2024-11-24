from flask import jsonify, request
from flask_restx import Namespace, Resource
from ..services.trivia_services import (
    get_all_trivias, create_new_trivia, get_trivia_by_id, update_trivia_by_id, delete_trivia_by_id,
    get_trivia_questions, get_trivia_ranking, submit_user_answers
)
from ..auth import token_required, admin_required

api = Namespace('trivias', description='Operaciones relacionadas con trivias')

@api.route("/")
class TriviaList(Resource):
    @token_required
    def get(self, current_user):
        try:
            result = get_all_trivias()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        question_ids = data.get('question_ids')
        user_ids = data.get('user_ids')
        try:
            create_new_trivia(name, description, question_ids, user_ids)
            return jsonify({"message": "Trivia creada exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:trivia_id>")
class Trivia(Resource):
    def get(self, trivia_id):
        try:
            trivia = get_trivia_by_id(trivia_id)
            return jsonify(trivia)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def put(self, trivia_id):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        question_ids = data.get('question_ids')
        user_ids = data.get('user_ids')
        try:
            update_trivia_by_id(trivia_id, name, description, question_ids, user_ids)
            return jsonify({"message": "Trivia actualizada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_required
    def delete(self, trivia_id):
        try:
            delete_trivia_by_id(trivia_id)
            return jsonify({"message": "Trivia eliminada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:trivia_id>/questions")
class TriviaQuestions(Resource):
    @token_required
    def get(self, current_user, trivia_id):
        try:
            result = get_trivia_questions(trivia_id)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:trivia_id>/ranking")
class TriviaRanking(Resource):
    def get(self, trivia_id):
        try:
            result = get_trivia_ranking(trivia_id)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api.route("/<int:trivia_id>/users/<int:user_id>/answers")
class SubmitAnswers(Resource):
    def post(self, trivia_id, user_id):
        data = request.get_json()
        answers = data.get('answers')
        try:
            score = submit_user_answers(trivia_id, user_id, answers)
            return jsonify({"message": "Respuestas enviadas exitosamente", "score": score}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
from flask import jsonify, request
from flask_restx import Namespace, Resource
from ..services.answer_services import submit_user_answers

api = Namespace('answers', description='Operaciones relacionadas con respuestas')

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
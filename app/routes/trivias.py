from flask import Blueprint, jsonify, request
from ..auth import admin_required, token_required
from ..services.user_service import get_user_by_id
from ..services.trivia_service import (create_new_trivia, 
                                       delete_trivia_by_id, 
                                       get_all_trivias, 
                                       get_trivia_by_id, 
                                       get_trivia_questions, 
                                       get_trivia_ranking, 
                                       get_trivias_for_user, 
                                       submit_user_answers, 
                                       update_trivia_by_id,) 

trivias_bp = Blueprint('trivias', __name__)

@trivias_bp.route("/trivias", methods=["GET"])
@token_required
def list_trivias(current_user):
    try:
        result = get_all_trivias()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@trivias_bp.route("/users/<int:user_id>/trivias", methods=["GET"])
@token_required
def list_trivias_for_user(current_user, user_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        result = get_trivias_for_user(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias/<int:trivia_id>/questions", methods=["GET"])
@token_required
def get_trivia_questions_route(current_user, trivia_id):
    try:
        trivia = get_trivia_by_id(trivia_id)
        if not trivia:
            return jsonify({"message": "Trivia no encontrada"}), 404
        
        result = get_trivia_questions(trivia_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias", methods=["POST"])
@admin_required
def create_trivia():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    question_ids = data.get('question_ids')
    user_ids = data.get('user_ids')
    
    if not name or not description or not question_ids or not user_ids:
        return jsonify({"message": "Nombre, descripción, preguntas y usuarios son requeridos"}), 400
    
    try:
        create_new_trivia(name, description, question_ids, user_ids)
        return jsonify({"message": "Trivia creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@trivias_bp.route("/trivias/<int:trivia_id>", methods=["GET"])
def get_trivia(trivia_id):
    try:
        trivia = get_trivia_by_id(trivia_id)
        if not trivia:
            return jsonify({"message": "Trivia no encontrada"}), 404
        return jsonify(trivia)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias/<int:trivia_id>", methods=["PUT"])
@admin_required
def update_trivia(trivia_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    question_ids = data.get('question_ids')
    user_ids = data.get('user_ids')
    
    if not name or not description or not question_ids or not user_ids:
        return jsonify({"message": "Nombre, descripción, preguntas y usuarios son requeridos"}), 400

    try:
        trivia = get_trivia_by_id(trivia_id)
        if not trivia:
            return jsonify({"message": "Trivia no encontrada"}), 404
        
        update_trivia_by_id(trivia_id, name, description, question_ids, user_ids)
        return jsonify({"message": "Trivia actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias/<int:trivia_id>/users/<int:user_id>/answers", methods=["POST"])
def submit_answers(trivia_id, user_id):
    data = request.get_json()
    answers = data.get('answers')
    
    if not answers:
       return jsonify({"message": "Las respuestas son requeridas"}), 400
    
    try:
        score = submit_user_answers(trivia_id, user_id, answers)
        return jsonify({"message": "Respuestas enviadas exitosamente", "score": score}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias/<int:trivia_id>/ranking", methods=["GET"])
def get_trivia_ranking_route(trivia_id):
    try:
        result = get_trivia_ranking(trivia_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trivias_bp.route("/trivias/<int:trivia_id>", methods=["DELETE"])
@admin_required
def delete_trivia(trivia_id):
    try:
        trivia = get_trivia_by_id(trivia_id)
        if not trivia:
            return jsonify({"message": "Trivia no encontrada"}), 404
        
        delete_trivia_by_id(trivia_id)
        return jsonify({"message": "Trivia eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@trivias_bp.route("/trivias/<int:trivia_id>/users/<int:user_id>/answers", methods=["DELETE"])
@token_required
def delete_user_answers(current_user, trivia_id, user_id):
    try:
        trivia = get_trivia_by_id(trivia_id)
        if not trivia:
            return jsonify({"message": "Trivia no encontrada"}), 404
        
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        delete_user_answers(trivia_id, user_id)
        return jsonify({"message": "Respuestas eliminadas exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
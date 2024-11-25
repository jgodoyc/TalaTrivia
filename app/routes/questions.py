from flask import Blueprint, jsonify, request
from ..auth import admin_required
from ..services.question_service import (create_new_question, delete_question_by_id, get_all_questions, get_question_by_id, update_question_by_id)

questions_bp = Blueprint('questions', __name__)

@questions_bp.route("/questions", methods=["GET"])
def list_questions():
    try:
        result = get_all_questions()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questions_bp.route("/questions", methods=["POST"])
@admin_required
def create_question():
    data = request.get_json()
    question = data.get('question')
    difficulty = data.get('difficulty')
    options = data.get('options')
    
    if not question or not difficulty or not options:
        return jsonify({"message": "Pregunta, dificultad y opciones son requeridos"}), 400
    
    try:
        create_new_question(question, difficulty, options)
        return jsonify({"message": "Pregunta creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@questions_bp.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    try:
        question = get_question_by_id(question_id)
        if not question:
            return jsonify({"message": "Pregunta no encontrada"}), 404        
        
        return jsonify(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questions_bp.route("/questions/<int:question_id>", methods=["PUT"])
@admin_required
def update_question(question_id):
    data = request.get_json()
    question = data.get('question')
    difficulty = data.get('difficulty')
    options = data.get('options')
    
    if not question or not difficulty or not options:
        return jsonify({"message": "Pregunta, dificultad y opciones son requeridos"}), 400
    
    try:
        question = get_question_by_id(question_id)
        if not question:
            return jsonify({"message": "Pregunta no encontrada"}), 404
        
        update_question_by_id(question_id, question, difficulty, options)
        return jsonify({"message": "Pregunta actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questions_bp.route("/questions/<int:question_id>", methods=["DELETE"])
@admin_required
def delete_question(question_id):
    try:
        question = get_question_by_id(question_id)
        if not question:
            return jsonify({"message": "Pregunta no encontrada"}), 404
        
        delete_question_by_id(question_id)
        return jsonify({"message": "Pregunta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
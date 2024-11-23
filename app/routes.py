from flask import Blueprint, jsonify, request
from .auth import generate_token, token_required
from .db import connection as get_connection
from .services import (
    get_all_users, create_new_user, get_all_questions, create_new_question,
    get_all_trivias, get_trivia_questions, create_new_trivia, submit_user_answers,
    get_trivia_ranking
)
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)

api = Blueprint('api', __name__)

def after_request(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@api.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Bienvenido a la Trivia API con Flask"})

@api.route("/test-db", methods=["GET"])
def test_db():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        connection.close()
        return jsonify({"message": "Conexión a la base de datos exitosa", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, email FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
        connection.close()
        
        if user:
            token = generate_token(user['id']) 
            return jsonify({'token': token, 'userId': user['id']}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route("/users", methods=["GET"])
@token_required
def list_users(current_user):
    try:
        result = get_all_users()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/users", methods=["POST"])
@token_required
def create_user(current_user):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role', 'jugador')
    try:
        create_new_user(name, email, role)
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/questions", methods=["GET"])
def list_questions():
    try:
        result = get_all_questions()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()
    question = data.get('question')
    difficulty = data.get('difficulty')
    options = data.get('options')
    try:
        create_new_question(question, difficulty, options)
        return jsonify({"message": "Pregunta creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias", methods=["GET"])
@token_required
def list_trivias(current_user):
    try:
        result = get_all_trivias()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias/<int:trivia_id>/questions", methods=["GET"])
@token_required
def get_trivia_questions_route(current_user, trivia_id):
    try:
        result = get_trivia_questions(trivia_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias", methods=["POST"])
def create_trivia():
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

@api.route("/trivias/<int:trivia_id>/users/<int:user_id>/answers", methods=["POST"])
def submit_answers(trivia_id, user_id):
    data = request.get_json()
    answers = data.get('answers')  # Lista de respuestas con 'question_id' y 'selected_option_id'
    try:
        score = submit_user_answers(trivia_id, user_id, answers)
        return jsonify({"message": "Respuestas enviadas exitosamente", "score": score}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias/<int:trivia_id>/ranking", methods=["GET"])
def get_trivia_ranking_route(trivia_id):
    try:
        result = get_trivia_ranking(trivia_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
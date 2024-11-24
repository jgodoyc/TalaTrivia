from flask import Blueprint, jsonify, request
from .auth import generate_token, token_required
from .db import connection as get_connection
from .auth import admin_required
from .services import (
    get_all_users, create_new_user, get_user_by_id, update_user_by_id, delete_user_by_id,
    get_all_questions, create_new_question, get_question_by_id, update_question_by_id, delete_question_by_id,
    get_all_trivias, create_new_trivia, get_trivia_by_id, update_trivia_by_id, delete_trivia_by_id,
    get_all_questions, create_new_question, get_option_by_id, update_option_by_id, delete_option_by_id,
    submit_user_answers, get_trivia_ranking, get_trivia_questions, get_trivias_for_user
)

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
            cursor.execute("SELECT id, email, role FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
        connection.close()
        
        if user:
            token = generate_token(user['id']) 
            return jsonify({'token': token, 'userId': user['id'], 'role': user['role']}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#### Users
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

@api.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(current_user, user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/users/<int:user_id>", methods=["PUT"])
@token_required
def update_user(current_user, user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    try:
        update_user_by_id(user_id, name, email, role)
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, user_id):
    try:
        delete_user_by_id(user_id)
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#### Questions    
@api.route("/questions", methods=["GET"])
def list_questions():
    try:
        result = get_all_questions()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/questions", methods=["POST"])
@admin_required
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
    
@api.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    try:
        question = get_question_by_id(question_id)
        return jsonify(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/questions/<int:question_id>", methods=["PUT"])
@admin_required
def update_question(question_id):
    data = request.get_json()
    question = data.get('question')
    difficulty = data.get('difficulty')
    options = data.get('options')
    try:
        update_question_by_id(question_id, question, difficulty, options)
        return jsonify({"message": "Pregunta actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/questions/<int:question_id>", methods=["DELETE"])
@admin_required
def delete_question(question_id):
    try:
        delete_question_by_id(question_id)
        return jsonify({"message": "Pregunta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#### Trivias
@api.route("/trivias", methods=["GET"])
@token_required
def list_trivias(current_user):
    try:
        result = get_all_trivias()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/users/<int:user_id>/trivias", methods=["GET"])
@token_required
def list_trivias_for_user(current_user, user_id):
    try:
        result = get_trivias_for_user(user_id)
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
@admin_required
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
@admin_required
def submit_answers(trivia_id, user_id):
    data = request.get_json()
    answers = data.get('answers')
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
    
@api.route("/trivias/<int:trivia_id>", methods=["GET"])
def get_trivia(trivia_id):
    try:
        trivia = get_trivia_by_id(trivia_id)
        return jsonify(trivia)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias/<int:trivia_id>", methods=["PUT"])
@admin_required
def update_trivia(trivia_id):
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

@api.route("/trivias/<int:trivia_id>", methods=["DELETE"])
@admin_required
def delete_trivia(trivia_id):
    try:
        delete_trivia_by_id(trivia_id)
        return jsonify({"message": "Trivia eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

###Options
@api.route("/options/<int:option_id>", methods=["GET"])
def get_option(option_id):
    try:
        option = get_option_by_id(option_id)
        return jsonify(option)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/options/<int:option_id>", methods=["PUT"])
@admin_required
def update_option(option_id):
    data = request.get_json()
    option_text = data.get('option_text')
    is_correct = data.get('is_correct')
    try:
        update_option_by_id(option_id, option_text, is_correct)
        return jsonify({"message": "Opción actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/options/<int:option_id>", methods=["DELETE"])
@admin_required
def delete_option(option_id):
    try:
        delete_option_by_id(option_id)
        return jsonify({"message": "Opción eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
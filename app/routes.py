from flask import Blueprint, jsonify, request
from .db import connection as get_connection

api = Blueprint('api', __name__)

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

@api.route("/users", methods=["GET"])
def list_users():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()
        connection.close()
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/questions", methods=["GET"])
def list_questions():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM questions")
            result = cursor.fetchall()
        connection.close()
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
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO questions (question, difficulty) VALUES (%s, %s)", (question, difficulty))
            question_id = cursor.lastrowid
            for option in options:
                cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)", 
                               (question_id, option['option_text'], option['is_correct']))
            connection.commit()
        connection.close()
        return jsonify({"message": "Pregunta creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias", methods=["GET"])
def list_trivias():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trivias")
            result = cursor.fetchall()
        connection.close()
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
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO trivias (name, description) VALUES (%s, %s)", (name, description))
            trivia_id = cursor.lastrowid
            for question_id in question_ids:
                cursor.execute("INSERT INTO trivia_questions (trivia_id, question_id) VALUES (%s, %s)", 
                               (trivia_id, question_id))
            for user_id in user_ids:
                cursor.execute("INSERT INTO trivia_users (trivia_id, user_id) VALUES (%s, %s)", 
                               (trivia_id, user_id))
            connection.commit()
        connection.close()
        return jsonify({"message": "Trivia creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@api.route("/trivias/<int:trivia_id>/users/<int:user_id>", methods=["GET"])
def get_trivia_for_user(trivia_id, user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT q.id, q.question, o.id as option_id, o.option_text 
                FROM trivia_questions tq
                JOIN questions q ON tq.question_id = q.id
                JOIN options o ON q.id = o.question_id
                WHERE tq.trivia_id = %s
            """, (trivia_id,))
            result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias/<int:trivia_id>/users/<int:user_id>/answers", methods=["POST"])
def submit_answers(trivia_id, user_id):
    data = request.get_json()
    answers = data.get('answers')  # Lista de respuestas con 'question_id' y 'selected_option_id'
    try:
        connection = get_connection()
        score = 0
        with connection.cursor() as cursor:
            for answer in answers:
                cursor.execute("INSERT INTO user_answers (user_id, question_id, selected_option_id) VALUES (%s, %s, %s)", 
                               (user_id, answer['question_id'], answer['selected_option_id']))
                cursor.execute("SELECT is_correct, difficulty FROM options o JOIN questions q ON o.question_id = q.id WHERE o.id = %s", 
                               (answer['selected_option_id'],))
                result = cursor.fetchone()
                if result['is_correct']:
                    if result['difficulty'] == 'easy':
                        score += 1
                    elif result['difficulty'] == 'medium':
                        score += 2
                    elif result['difficulty'] == 'hard':
                        score += 3
            cursor.execute("INSERT INTO user_scores (user_id, trivia_id, score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE score = %s", 
                           (user_id, trivia_id, score, score))
            connection.commit()
        connection.close()
        return jsonify({"message": "Respuestas enviadas exitosamente", "score": score}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/trivias/<int:trivia_id>/ranking", methods=["GET"])
def get_trivia_ranking(trivia_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.name, us.score 
                FROM user_scores us
                JOIN users u ON us.user_id = u.id
                WHERE us.trivia_id = %s
                ORDER BY us.score DESC
            """, (trivia_id,))
            result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
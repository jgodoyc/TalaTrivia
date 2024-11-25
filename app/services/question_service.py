from ..db import connection as get_connection

def get_all_questions():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM questions")
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener las preguntas: {str(e)}")
    finally:
        connection.close()

def create_new_question(question, difficulty, options):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO questions (question, difficulty) VALUES (%s, %s)", (question, difficulty))
            question_id = cursor.lastrowid
            for option in options:
                cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)", 
                               (question_id, option['option_text'], option['is_correct']))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al crear la pregunta: {str(e)}")
    finally:
        connection.close()

def get_question_by_id(question_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
            result = cursor.fetchone()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener la pregunta: {str(e)}")
    finally:
        connection.close()

def update_question_by_id(question_id, question, difficulty, options):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE questions SET question = %s, difficulty = %s WHERE id = %s", (question, difficulty, question_id))
            cursor.execute("DELETE FROM options WHERE question_id = %s", (question_id,))
            for option in options:
                cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)", 
                               (question_id, option['option_text'], option['is_correct']))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al actualizar la pregunta: {str(e)}")
    finally:
        connection.close()

def delete_question_by_id(question_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al eliminar la pregunta: {str(e)}")
    finally:
        connection.close()
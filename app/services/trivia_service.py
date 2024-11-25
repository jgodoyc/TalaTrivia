from ..db import connection as get_connection

def get_all_trivias():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trivias")
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener las trivias: {str(e)}")
    finally:
        connection.close()

def get_trivias_for_user(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.id, t.name, t.description
                FROM trivias t
                JOIN trivia_users tu ON t.id = tu.trivia_id
                WHERE tu.user_id = %s
            """, (user_id,))
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener las trivias para el usuario: {str(e)}")
    finally:
        connection.close()

def get_trivia_questions(trivia_id):
    connection = get_connection()
    try:
        questions = {}
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT q.id, q.question, q.difficulty, o.id as option_id, o.option_text, o.is_correct
                FROM trivia_questions tq
                JOIN questions q ON tq.question_id = q.id
                JOIN options o ON q.id = o.question_id
                WHERE tq.trivia_id = %s
                ORDER BY RAND()
            """, (trivia_id,))
            result = cursor.fetchall()
            
            for row in result:
                question_id = row['id']
                if question_id not in questions:
                    questions[question_id] = {
                        'id': question_id,
                        'question': row['question'],
                        'difficulty': row['difficulty'],
                        'options': []
                    }
                questions[question_id]['options'].append({
                    'id': row['option_id'],
                    'option_text': row['option_text'],
                    'is_correct': row['is_correct']
                })
        return list(questions.values())
    except Exception as e:
        raise Exception(f"Error al obtener las preguntas de la trivia: {str(e)}")
    finally:
        connection.close()

def create_new_trivia(name, description, question_ids, user_ids):
    connection = get_connection()
    try:
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
    except Exception as e:
        raise Exception(f"Error al crear la trivia: {str(e)}")
    finally:
        connection.close()

def get_trivia_by_id(trivia_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trivias WHERE id = %s", (trivia_id,))
            result = cursor.fetchone()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener la trivia: {str(e)}")
    finally:
        connection.close()

def update_trivia_by_id(trivia_id, name, description, question_ids, user_ids):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE trivias SET name = %s, description = %s WHERE id = %s", (name, description, trivia_id))
            cursor.execute("DELETE FROM trivia_questions WHERE trivia_id = %s", (trivia_id,))
            for question_id in question_ids:
                cursor.execute("INSERT INTO trivia_questions (trivia_id, question_id) VALUES (%s, %s)", 
                               (trivia_id, question_id))
            cursor.execute("DELETE FROM trivia_users WHERE trivia_id = %s", (trivia_id,))
            for user_id in user_ids:
                cursor.execute("INSERT INTO trivia_users (trivia_id, user_id) VALUES (%s, %s)", 
                               (trivia_id, user_id))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al actualizar la trivia: {str(e)}")
    finally:
        connection.close()

def delete_trivia_by_id(trivia_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM trivias WHERE id = %s", (trivia_id,))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al eliminar la trivia: {str(e)}")
    finally:
        connection.close()

def get_trivia_ranking(trivia_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT u.id, u.name, MAX(us.score) as score
            FROM user_scores us
            JOIN users u ON us.user_id = u.id
            WHERE us.trivia_id = %s
            GROUP BY u.id, u.name
            ORDER BY score DESC
            """, (trivia_id,))
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener el ranking de la trivia: {str(e)}")
    finally:
        connection.close()

def submit_user_answers(trivia_id, user_id, answers):
    connection = get_connection()
    try:
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
        return score
    except Exception as e:
        raise Exception(f"Error al enviar las respuestas del usuario: {str(e)}")
    finally:
        connection.close()
from ..db import connection as get_connection

def get_all_trivias():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM trivias")
        result = cursor.fetchall()
    connection.close()
    return result

def create_new_trivia(name, description, question_ids, user_ids):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO trivias (name, description) VALUES (%s, %s)", (name, description))
        trivia_id = cursor.lastrowid
        for question_id in question_ids:
            cursor.execute("INSERT INTO trivia_questions (trivia_id, question_id) VALUES (%s, %s)", (trivia_id, question_id))
        for user_id in user_ids:
            cursor.execute("INSERT INTO trivia_users (trivia_id, user_id) VALUES (%s, %s)", (trivia_id, user_id))
        connection.commit()
    connection.close()

def get_trivia_by_id(trivia_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM trivias WHERE id = %s", (trivia_id,))
        result = cursor.fetchone()
    connection.close()
    return result

def update_trivia_by_id(trivia_id, name, description, question_ids, user_ids):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE trivias SET name = %s, description = %s WHERE id = %s", (name, description, trivia_id))
        cursor.execute("DELETE FROM trivia_questions WHERE trivia_id = %s", (trivia_id,))
        cursor.execute("DELETE FROM trivia_users WHERE trivia_id = %s", (trivia_id,))
        for question_id in question_ids:
            cursor.execute("INSERT INTO trivia_questions (trivia_id, question_id) VALUES (%s, %s)", (trivia_id, question_id))
        for user_id in user_ids:
            cursor.execute("INSERT INTO trivia_users (trivia_id, user_id) VALUES (%s, %s)", (trivia_id, user_id))
        connection.commit()
    connection.close()

def delete_trivia_by_id(trivia_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM trivias WHERE id = %s", (trivia_id,))
        connection.commit()
    connection.close()

def get_trivia_questions(trivia_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM questions WHERE id IN (SELECT question_id FROM trivia_questions WHERE trivia_id = %s)", (trivia_id,))
        result = cursor.fetchall()
    connection.close()
    return result

def get_trivia_ranking(trivia_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT users.name, scores.score FROM scores JOIN users ON scores.user_id = users.id WHERE scores.trivia_id = %s ORDER BY scores.score DESC", (trivia_id,))
        result = cursor.fetchall()
    connection.close()
    return result

def submit_user_answers(trivia_id, user_id, answers):
    connection = get_connection()
    score = 0
    with connection.cursor() as cursor:
        for answer in answers:
            cursor.execute("SELECT is_correct FROM options WHERE id = %s", (answer['selected_option_id'],))
            result = cursor.fetchone()
            if result['is_correct']:
                score += 1
        cursor.execute("INSERT INTO scores (user_id, trivia_id, score) VALUES (%s, %s, %s)", (user_id, trivia_id, score))
        connection.commit()
    connection.close()
    return score
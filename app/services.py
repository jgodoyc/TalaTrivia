from .db import connection as get_connection

def get_all_users():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
    connection.close()
    return result

def create_new_user(name, email, role):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email, role) VALUES (%s, %s, %s)", (name, email, role))
        connection.commit()
    connection.close()

def get_all_questions():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM questions")
        result = cursor.fetchall()
    connection.close()
    return result

def create_new_question(question, difficulty, options):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO questions (question, difficulty) VALUES (%s, %s)", (question, difficulty))
        question_id = cursor.lastrowid
        for option in options:
            cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)", 
                           (question_id, option['option_text'], option['is_correct']))
        connection.commit()
    connection.close()

def get_all_trivias():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM trivias")
        result = cursor.fetchall()
    connection.close()
    return result

def get_trivia_questions(trivia_id):
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
    questions = {}
    for row in result:
        if row['id'] not in questions:
            questions[row['id']] = {
                'id': row['id'],
                'question': row['question'],
                'options': []
            }
        questions[row['id']]['options'].append({
            'id': row['option_id'],
            'option_text': row['option_text']
        })
    return list(questions.values())

def create_new_trivia(name, description, question_ids, user_ids):
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

def submit_user_answers(trivia_id, user_id, answers):
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
    return score

def get_trivia_ranking(trivia_id):
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
    return result
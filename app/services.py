from .db import connection as get_connection

###Users
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
    
def get_user_by_id(user_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
    connection.close()
    return result

def update_user_by_id(user_id, name, email, role):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE users SET name = %s, email = %s, role = %s WHERE id = %s", (name, email, role, user_id))
        connection.commit()
    connection.close()

def delete_user_by_id(user_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
    connection.close()

###Questions
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
    
def get_question_by_id(question_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        result = cursor.fetchone()
    connection.close()
    return result

def update_question_by_id(question_id, question, difficulty, options):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE questions SET question = %s, difficulty = %s WHERE id = %s", (question, difficulty, question_id))
        cursor.execute("DELETE FROM options WHERE question_id = %s", (question_id,))
        for option in options:
            cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)", 
                           (question_id, option['option_text'], option['is_correct']))
        connection.commit()
    connection.close()

def delete_question_by_id(question_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
        connection.commit()
    connection.close()

###Trivias
def get_all_trivias():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM trivias")
        result = cursor.fetchall()
    connection.close()
    return result

def get_trivia_questions(trivia_id):
    connection = get_connection()
    questions = {}
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT q.id, q.question, q.difficulty, o.id as option_id, o.option_text, o.is_correct
            FROM trivia_questions tq
            JOIN questions q ON tq.question_id = q.id
            JOIN options o ON q.id = o.question_id
            WHERE tq.trivia_id = %s
            ORDER BY q.id, RAND()
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
    
    connection.close()
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
        for question_id in question_ids:
            cursor.execute("INSERT INTO trivia_questions (trivia_id, question_id) VALUES (%s, %s)", 
                           (trivia_id, question_id))
        cursor.execute("DELETE FROM trivia_users WHERE trivia_id = %s", (trivia_id,))
        for user_id in user_ids:
            cursor.execute("INSERT INTO trivia_users (trivia_id, user_id) VALUES (%s, %s)", 
                           (trivia_id, user_id))
        connection.commit()
    connection.close()

def delete_trivia_by_id(trivia_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM trivias WHERE id = %s", (trivia_id,))
        connection.commit()
    connection.close()

###Options
def get_option_by_id(option_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM options WHERE id = %s", (option_id,))
        result = cursor.fetchone()
    connection.close()
    return result

def update_option_by_id(option_id, option_text, is_correct):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE options SET option_text = %s, is_correct = %s WHERE id = %s", (option_text, is_correct, option_id))
        connection.commit()
    connection.close()

def delete_option_by_id(option_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM options WHERE id = %s", (option_id,))
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
            SELECT u.id, u.name, MAX(us.score) as score
            FROM user_scores us
            JOIN users u ON us.user_id = u.id
            WHERE us.trivia_id = %s
            GROUP BY u.id, u.name
            ORDER BY score DESC
        """, (trivia_id,))
        result = cursor.fetchall()
    connection.close()
    return result
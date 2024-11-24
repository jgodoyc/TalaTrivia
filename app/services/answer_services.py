from ..db import connection as get_connection

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
from ..db import connection as get_connection

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
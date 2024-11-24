from ..db import connection as get_connection

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
from ..db import connection as get_connection

def get_all_users():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email, role FROM users")
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener los usuarios: {str(e)}")
    finally:
        connection.close()

def create_new_user(name, email, password, role):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", (name, email, password, role))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al crear el usuario: {str(e)}")
    finally:
        connection.close()

def get_user_by_id(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
        return result
    except Exception as e:
        raise Exception(f"Error al obtener el usuario: {str(e)}")
    finally:
        connection.close()

def update_user_by_id(user_id, name, email, password, role):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET name = %s, email = %s, password = %s, role = %s WHERE id = %s", 
                           (name, email, password, role, user_id))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al actualizar el usuario: {str(e)}")
    finally:
        connection.close()

def delete_user_by_id(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error al eliminar el usuario: {str(e)}")
    finally:
        connection.close()
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('MYSQL_HOST')
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DB')
DB_PORT = int(os.getenv('MYSQL_PORT'))
DB_CHARSET = os.getenv('MYSQL_DATABASE_CHARSET')

def connection():
    """Crea y devuelve una conexión a la base de datos MySQL."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset=DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

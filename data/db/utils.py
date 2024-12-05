import platform
import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

def get_print_time():
    import time
    return time.strftime(r'%m.%d.%Y %H:%M:%S', time.localtime())


def create_db_connection(timeout=30):
    try:
        connection = psycopg2.connect(
            host=DB_CREDENTIALS['host'],
            port=DB_CREDENTIALS['port'],
            database=DB_CREDENTIALS['database'],
            user=DB_CREDENTIALS['user'],
            password=DB_CREDENTIALS['password']
        )
        print(f"[{get_print_time()}] PostgreSQL database connection established.")
        return connection

    except OperationalError as e:
        error_message = str(e)

        if 'timeout' in error_message.lower() or 'could not connect' in error_message.lower():
            print(f"[{get_print_time()}] Error: Connection attempt timed out after {timeout} seconds.")
        else:
            print(f"[{get_print_time()}] Error: Failed to create PostgreSQL database connection. \n{e}")

        raise ConnectionError

    except Exception as e:
        print(f"[{get_print_time()}] Unexpected Error: {e}")

        raise ConnectionError


def close_db_connection(connection):
    try:
        connection.close()
        print(f"[{get_print_time()}] PostgreSQL database connection closed.")
    except psycopg2.Error as e:
        print(f"[{get_print_time()}] Error: Failed to close database connection. \n{e}")


def execute_query(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error: Query execution failed. \n{e}")


sys_platform = platform.system()

if sys_platform == 'Darwin':
    PATH = '/Users/yichizhang/Documents/Code/quick_escape'

elif sys_platform == 'Linux':
    PATH = '/root/QuickEscape'

else:
    PATH = ''
    print(f"Unknown platform {sys_platform}")

load_dotenv()

DB_CREDENTIALS = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
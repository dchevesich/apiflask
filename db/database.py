import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
import os
from dotenv import load_dotenv

load_dotenv('config/.env')


def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return None


def ejecutar_query(query, params=None, fetch=True):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)

        if fetch:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount

        conn.commit()
        return result

    except errors.UniqueViolation as e:
        print(f"Registro duplicado: {e}")
        if conn:
            conn.rollback()
        return None

    except errors.ForeignKeyViolation as e:
        print(f"FK no existe: {e}")
        if conn:
            conn.rollback()
        return None

    except errors.NotNullViolation as e:
        print(f"Campo obligatorio falta: {e}")
        if conn:
            conn.rollback()
        return None

    except Exception as e:
        print(f"Error ejecutando query: {e}")
        if conn:
            conn.rollback()
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

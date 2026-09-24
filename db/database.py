import atexit
import os
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

BASE_DIR = Path(__file__).resolve().parent.parent
for env_path in (BASE_DIR / ".env", BASE_DIR / "config" / ".env", BASE_DIR / ".env.prod"):
    if env_path.is_file():
        load_dotenv(env_path, override=True)
        break


_connection_pool = None
_pool_lock = Lock()


def _get_pool():
    global _connection_pool

    with _pool_lock:
        if _connection_pool is None:
            required_settings = ("DB_HOST", "DB_PORT",
                                 "DB_NAME", "DB_USER", "DB_PASSWORD")
            missing_settings = [
                setting for setting in required_settings if not os.getenv(setting)
            ]
            if missing_settings:
                raise RuntimeError(
                    "Faltan variables de conexión a la BD: "
                    + ", ".join(missing_settings)
                )

            min_connections = int(os.getenv("DB_POOL_MIN", "1"))
            max_connections = int(os.getenv("DB_POOL_MAX", "5"))
            if min_connections < 1 or max_connections < min_connections:
                raise ValueError(
                    "DB_POOL_MIN y DB_POOL_MAX tienen valores inválidos")

            _connection_pool = ThreadedConnectionPool(
                min_connections,
                max_connections,
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
            )

        return _connection_pool


def get_connection():
    try:
        return _get_pool().getconn()
    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return None


def _release_connection(conn, close=False):
    if conn is None:
        return

    try:
        _get_pool().putconn(conn, close=close or conn.closed)
    except Exception as e:
        print(f"Error devolviendo conexión al pool: {e}")


def close_pool():
    global _connection_pool

    with _pool_lock:
        if _connection_pool is not None:
            _connection_pool.closeall()
            _connection_pool = None


atexit.register(close_pool)


def ejecutar_query(query, params=None, fetch=True):
    conn = None
    cursor = None
    discard_connection = False

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
        discard_connection = True
        if conn:
            conn.rollback()
        return None

    except errors.ForeignKeyViolation as e:
        print(f"FK no existe: {e}")
        discard_connection = True
        if conn:
            conn.rollback()
        return None

    except errors.NotNullViolation as e:
        print(f"Campo obligatorio falta: {e}")
        discard_connection = True
        if conn:
            conn.rollback()
        return None

    except Exception as e:
        print(f"Error ejecutando query: {e}")
        discard_connection = True
        if conn:
            conn.rollback()
        return None

    finally:
        if cursor:
            cursor.close()
        _release_connection(conn, close=discard_connection)

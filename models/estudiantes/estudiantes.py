from db import database


class Estudiantes:

    @staticmethod
    def get_estudiante():
        q = """
            SELECT idestudiante, nombre, email, telefono FROM estudiantes
            """
        return database.ejecutar_query(q)

    @staticmethod
    def get_estudiante_id(idestudiante):
        q = """
            SELECT idestudiante, nombre, email, telefono FROM estudiantes
            WHERE idestudiante = %s
            """
        return database.ejecutar_query(q, (idestudiante,))

    @staticmethod
    def existe_email(email):
        q = """
            SELECT 1 FROM estudiantes
            WHERE email = %s
            LIMIT 1
            """
        result = database.ejecutar_query(q, (email,))
        return bool(result)

    @staticmethod
    def post_estudiantes(data):
        q = """
            INSERT INTO estudiantes (nombre, email, telefono)
            VALUES (%s, %s, %s)
            RETURNING idestudiante
            """
        prms = (
            data.get("nombre"),
            data.get("email"),
            data.get("telefono")
        )
        return database.ejecutar_query(q, prms)

    @staticmethod
    def delete_estudiantes(idestudiante):
        q = """
            DELETE FROM estudiantes 
            WHERE idestudiante = %s;
            """

        return database.ejecutar_query(q, (idestudiante,), fetch=False)

    @staticmethod
    def actualizar_estudiantes(data, idestudiante):
        q = """
            UPDATE estudiantes
            SET nombre = %s,
            email = %s,
            telefono = %s
            WHERE idestudiante = %s
            """
        prms = (
            data.get("nombre"),
            data.get("email"),
            data.get("telefono"),
            idestudiante,
        )

        return database.ejecutar_query(q, prms, fetch=False)

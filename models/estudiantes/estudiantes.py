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

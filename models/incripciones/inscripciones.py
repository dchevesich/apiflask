from db import database


class Incripciones:

    @staticmethod
    def obtener_incripciones():
        q = """
            SELECT 
            i.idinscripcion,
            i.idestudiante,
            i.idcurso,
            i.progreso_porcentaje,
            i.estado,
            e.nombre,
            c.titulo
        FROM inscripciones i
        JOIN estudiantes e ON i.idestudiante = e.idestudiante
        JOIN cursos c ON i.idcurso = c.idcurso
            """
        return database.ejecutar_query(q)

    @staticmethod
    def obtener_incripcionesId(idinscripcion):
        q = """
            SELECT 
            i.idinscripcion,
            i.idestudiante,
            i.idcurso,
            i.progreso_porcentaje,
            i.estado,
            e.nombre,
            c.titulo
        FROM inscripciones i
        JOIN estudiantes e ON i.idestudiante = e.idestudiante
        JOIN cursos c ON i.idcurso = c.idcurso
        WHERE idinscripcion = %s
            """
        return database.ejecutar_query(q, (idinscripcion,))

    @staticmethod
    def crear_inscripcion(idestudiante, idcurso, data):
        q = """
            INSERT INTO inscripciones (
                idestudiante,
                idcurso,
                fecha_inscripcion,
                fecha_inicio,
                fecha_finalizacion,
                progreso_porcentaje,
                estado,
                calificacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING idinscripcion
            """

        prms = (
            idestudiante,
            idcurso,
            data.get("fecha_inscripcion"),
            data.get("fecha_inicio"),
            data.get("fecha_finalizacion"),
            data.get("progreso_porcentaje"),
            data.get("estado"),
            data.get("calificacion")
        )
        return database.ejecutar_query(q, prms)

    @staticmethod
    def actualizar_inscripciones(data, idinscripcion):
        q = """
            UPDATE inscripciones
            SET fecha_inscripcion = %s,
            fecha_inicio = %s,
            fecha_finalizacion = %s,
            progreso_porcentaje = %s,
            estado = %s,
            calificacion = %s
            WHERE idinscripcion = %s
            """
        prms = (
            data.get("fecha_inscripcion"),
            data.get("fecha_inicio"),
            data.get("fecha_finalizacion"),
            data.get("progreso_porcentaje"),
            data.get("estado"),
            data.get("calificacion"),
            idinscripcion
        )

        return database.ejecutar_query(q, prms, fetch=False)

    @staticmethod
    def eliminar_inscripciones(idinscripcion):
        q = """
            DELETE FROM inscripciones 
            WHERE idinscripcion = %s;
            """

        return database.ejecutar_query(q, (idinscripcion,), fetch=False)

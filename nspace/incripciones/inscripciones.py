from flask_restx import Namespace, Resource
from models.incripciones import inscripciones

name_space = Namespace(
    "inscripciones", description="Clase para manejo de inscripciones")


@name_space.route("/")
class EstudianteGet(Resource):
    def get(self):
        response = inscripciones.Incripciones.obtener_incripciones()
        if not response:
            return {"message": "Inscripción no encontrada"}, 404
        return response, 200

    def post(self):
        data = name_space.payload or {}
        idestudiante = data.get("idestudiante")
        idcurso = data.get("idcurso")
        if not idestudiante or not idcurso:
            return {"message": "idestudiante y idcurso son obligatorios"}, 400
        response = inscripciones.Incripciones.crear_inscripcion(
            idestudiante, idcurso, data)
        if not response:
            return {"message": "Error al crear una inscripcion"}, 500
        return {
            "message": "Inscripcion creada correctamente",
            "idinscripcion": response[0]["idinscripcion"]
        }, 201


@name_space.route("/<int:idinscripcion>")
class EstudianteGetId(Resource):
    def get(self, idinscripcion):
        response = inscripciones.Incripciones.obtener_incripcionesId(
            idinscripcion)
        if not response:
            return {"message": "Inscripción no encontrada"}, 404
        return response[0], 200

    def put(self, idinscripcion):
        data = name_space.payload or {}
        response = inscripciones.Incripciones.actualizar_inscripciones(
            data, idinscripcion)

        if not response:
            return {"message": "Error al actualizar Inscripciones"}, 400
        return {"message": "Inscripcion actualizado"}, 200

    def delete(self, idinscripcion):
        response = inscripciones.Incripciones.eliminar_inscripciones(
            idinscripcion)
        if not response:
            return {"message": "Inscripcion no encontrada con el id proporcionado"}, 404
        return {
            "message": "Inscripcion eliminada."}, 200

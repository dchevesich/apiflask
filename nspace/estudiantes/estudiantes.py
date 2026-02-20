from flask_restx import Namespace, Resource
from models.estudiantes import estudiantes


name_space = Namespace(
    "estudiantes", description="Clase para manejo de estudiantes")


@name_space.route("/")
class EstudianteGet(Resource):
    def get(self):
        response = estudiantes.Estudiantes.get_estudiante()
        if not response:
            return [], 200
        return response, 200


@name_space.route("/<int:idestudiante>")
class EstudianteGetId(Resource):
    def get(self, idestudiante):
        response = estudiantes.Estudiantes.get_estudiante_id(idestudiante)
        if not response:
            return {"message": "Estudiante no encontrado"}, 404
        return response[0], 200

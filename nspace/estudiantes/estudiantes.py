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

    def post(self):
        data = name_space.payload or {}

        nombre = data.get("nombre")
        email = data.get("email")

        if not nombre or not email:
            return {"message": "nombre y email son obligatorios"}, 400

        if estudiantes.Estudiantes.existe_email(email):
            return {"message": "El email ya está registrado"}, 409

        response = estudiantes.Estudiantes.post_estudiantes(data)
        if not response:
            return {"message": "Error al crear un estudiante"}, 500
        return {
            "message": "Estudiante creado correctamente",
            "idestudiante": response[0]["idestudiante"]
        }, 201


@name_space.route("/<int:idestudiante>")
class EstudianteGetId(Resource):
    def get(self, idestudiante):
        response = estudiantes.Estudiantes.get_estudiante_id(idestudiante)
        if not response:
            return {"message": "Estudiante no encontrado"}, 404
        return response[0], 200

    def delete(self, idestudiante):
        response = estudiantes.Estudiantes.delete_estudiantes(idestudiante)
        if not response:
            return {"message": "Estudiante no encontrado con el id proporcionado"}, 404
        return {
            "message": "Estudiante eliminado."}, 200

    def put(self, idestudiante):
        data = name_space.payload or {}

        nombre = data.get("nombre")
        email = data.get("email")

        if not nombre or not email:
            return {"message": "nombre y email son obligatorios"}, 400

        response = estudiantes.Estudiantes.actualizar_estudiantes(
            data, idestudiante)

        if not response:
            return {"message": "Error al actualizar estudiante"}, 400
        return {"message": "Estudiante actualizado"}, 200

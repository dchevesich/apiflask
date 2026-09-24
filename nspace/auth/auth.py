from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash

from db.database import ejecutar_query


name_space = Namespace("auth", description="Autenticación de usuarios")

login_model = name_space.model("Login", {
    "username": fields.String(required=True, description="Nombre de usuario"),
    "password": fields.String(required=True, description="Contraseña"),
})


@name_space.route("/login")
class Login(Resource):
    @name_space.expect(login_model, validate=True)
    def post(self):
        data = name_space.payload
        users = ejecutar_query(
            """
            SELECT idusuario, username, password, nombre, email, rol
            FROM usuarios
            WHERE username = %s AND activo = TRUE
            """,
            (data["username"],),
        )

        if not users or not check_password_hash(users[0]["password"], data["password"]):
            return {"message": "Credenciales inválidas"}, 401

        user = users[0]
        token = create_access_token(
            identity=str(user["idusuario"]),
            additional_claims={"rol": user["rol"]},
        )
        return {
            "access_token": token,
            "user": {
                "idusuario": user["idusuario"],
                "username": user["username"],
                "nombre": user["nombre"],
                "email": user["email"],
                "rol": user["rol"],
            },
        }, 200

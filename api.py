import importlib
import os

from flask import Flask
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
jwt = JWTManager(app)


@jwt.unauthorized_loader
def handle_missing_token(error):
    return {"message": error}, 401


@jwt.invalid_token_loader
def handle_invalid_token(error):
    return {"message": error}, 401


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return {"message": "El token ha expirado"}, 401


api = Api(app, title="Tasks API", version="1.0",
          authorizations={
              "Bearer": {
                  "type": "apiKey",
                  "in": "header",
                  "name": "Authorization",
                  "description": "Escribe: Bearer {token}",
              }
          }, security="Bearer")


@api.errorhandler(JWTExtendedException)
def handle_jwt_error(error):
    return {"message": str(error)}, 401


try:
    auth_module = importlib.import_module("nspace.auth.auth")
    api.add_namespace(auth_module.name_space)
except Exception as error:
    print(f"Error cargando namespace de autenticación: {error}")
    raise

try:
    estudiantes_module = importlib.import_module(
        "nspace.estudiantes.estudiantes")
    api.add_namespace(estudiantes_module.name_space)
except Exception as error:
    print(f"Error cargando namespace de estudiantes: {error}")
    raise

try:
    incripciones_module = importlib.import_module(
        "nspace.incripciones.inscripciones")
    api.add_namespace(incripciones_module.name_space)
except Exception as error:
    print(f"Error cargando namespace de inscripciones: {error}")
    raise


if __name__ == "__main__":
    app.run(debug=True)

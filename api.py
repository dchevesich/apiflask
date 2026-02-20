import importlib
from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, title="Tasks API", version="1.0")

try:
    estudiantes_module = importlib.import_module(
        "nspace.estudiantes.estudiantes")
    api.add_namespace(estudiantes_module.name_space)
except Exception as error:
    print(f"Error cargando namespace de estudiantes: {error}")
    raise


if __name__ == "__main__":
    app.run(debug=True)

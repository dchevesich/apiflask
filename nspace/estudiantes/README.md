# Namespace de estudiantes

Este modulo expone las operaciones HTTP para consultar y administrar estudiantes.

## Ubicacion

- Namespace HTTP: `nspace/estudiantes/estudiantes.py`
- Acceso a datos: `models/estudiantes/estudiantes.py`
- Conexion: `db/database.py`

## Rutas

| Metodo | Ruta                          | Autenticacion | Descripcion             |
| ------ | ----------------------------- | ------------- | ----------------------- |
| GET    | `/estudiantes/`               | No            | Lista estudiantes       |
| GET    | `/estudiantes/{idestudiante}` | No            | Obtiene un estudiante   |
| POST   | `/estudiantes/`               | JWT           | Crea un estudiante      |
| PUT    | `/estudiantes/{idestudiante}` | JWT           | Actualiza un estudiante |
| DELETE | `/estudiantes/{idestudiante}` | JWT           | Elimina un estudiante   |

## Body para crear y actualizar

Swagger documenta el modelo `Estudiante` con este formato:

```json
{
  "nombre": "Nombre del estudiante",
  "email": "correo@example.com",
  "telefono": "+56912345678"
}
```

`nombre` y `email` son obligatorios. `telefono` es opcional.

## Autorizacion

Para `POST`, `PUT` y `DELETE` se debe enviar:

```http
Authorization: Bearer <access_token>
```

El token se obtiene desde `POST /auth/login`. Actualmente se valida que el token sea correcto; la restriccion especifica por rol debe aplicarse cuando se definan las politicas administrativas. Por ejemplo, `DELETE` normalmente deberia limitarse al rol `admin`.

## Reglas de negocio

- `email` no puede repetirse.
- Las consultas usan parametros SQL.
- Las operaciones de escritura se ejecutan dentro del flujo centralizado de `database.ejecutar_query`.
- Las respuestas de errores de validacion usan HTTP `400`.
- Un email repetido devuelve HTTP `409`.

## Prueba rapida

1. Inicia la API y abre Swagger en `http://127.0.0.1:5000/`.
2. Ejecuta `POST /auth/login`.
3. Pulsa **Authorize** y usa `Bearer <access_token>`.
4. Ejecuta una operacion de escritura sobre estudiantes.

No incluyas contrasenas, tokens JWT ni archivos `.env` en commits.

# Instrucciones para agentes y colaboradores

## Contexto del proyecto

Este repositorio contiene una API Flask RESTX para un sistema de cursos online. El punto de entrada es `api.py`. La aplicacion registra los namespaces de autenticacion, estudiantes e inscripciones.

## Entorno local

- Usa el entorno virtual `venv`.
- Instala dependencias con `python -m pip install -r requirements.txt`.
- Usa `.env` para la configuracion local.
- No leas, imprimas, copies ni confirmes secretos de `.env` o `.env.prod`.
- Selecciona `venv\\Scripts\\python.exe` como interprete de VS Code.

## Base de datos

- La base local configurada es PostgreSQL.
- La conexion se administra en `db/database.py` mediante `ThreadedConnectionPool`.
- Las consultas deben usar parametros (`%s`) y no interpolar valores recibidos por HTTP.
- Las conexiones y cursores deben cerrarse o devolverse al pool en todos los caminos.
- No ejecutes cambios destructivos en la base sin confirmacion explicita.

## Objetivo de despliegue AWS

El destino previsto es una arquitectura de bajo coste con EC2 para la API y RDS PostgreSQL para la base de datos. S3 es opcional para archivos o backups. CloudFront no es requisito inicial para una API sin frontend ni contenido estatico; debe agregarse solo cuando exista una necesidad validada.

- Mantener RDS sin acceso publico cuando la red lo permita.
- Permitir 5432 solo desde el Security Group de EC2.
- Ejecutar Flask con Gunicorn, nunca con `debug=True` en produccion.
- Usar IAM Roles para acceder a S3.
- No guardar access keys, contrasenas ni `JWT_SECRET_KEY` en el repositorio.
- Usar una clave JWT diferente en cada entorno.
- Mantener el pool pequeno en instancias con recursos limitados.
- Revisar Free Tier, cuotas y alertas de facturacion antes del despliegue.

## API y autenticacion

- Swagger esta disponible en `/` y el documento OpenAPI en `/swagger.json`.
- El login esta en `POST /auth/login`.
- JWT se configura con `Flask-JWT-Extended`.
- Las operaciones de escritura de estudiantes requieren `Authorization: Bearer <token>`.
- El token contiene `idusuario` y `rol`.
- No agregues secretos JWT permanentes al codigo.
- La autenticacion y la autorizacion son responsabilidades distintas: valida el token y luego aplica el rol requerido para cada accion administrativa.

## Estilo de cambios

- Mantener la separacion entre `models` (acceso a datos) y `nspace` (HTTP y validacion de entrada).
- Reutilizar los patrones existentes antes de crear nuevas abstracciones.
- Mantener los cambios pequenos y no reformatear archivos no relacionados.
- No renombrar el paquete existente `incripciones` sin una migracion coordinada.
- Los nombres y mensajes actuales estan principalmente en espanol.

## Validacion minima

Antes de entregar cambios Python:

```powershell
venv\\Scripts\\python.exe -m py_compile api.py db\\database.py nspace\\auth\\auth.py nspace\\estudiantes\\estudiantes.py nspace\\incripciones\\inscripciones.py
venv\\Scripts\\python.exe -m pip check
```

Para cambios de Swagger, comprueba `/swagger.json`. Para cambios de base de datos, valida la consulta contra la base local sin imprimir credenciales, contrasenas, tokens o datos sensibles.

## Git

- Trabajar en una rama de funcionalidad.
- No hacer commit de `.env`, `.env.prod`, `venv`, caches, bytecode ni logs.
- Crear Pull Request hacia `main`.
- Despues del merge, actualizar la rama local con `git pull origin main`.

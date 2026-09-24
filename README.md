# Flask API de Cursos Online

API REST para gestionar estudiantes e inscripciones en un sistema de cursos online.

## Tecnologias

- Python
- Flask
- Flask-RESTX
- PostgreSQL
- psycopg2-binary
- Flask-JWT-Extended
- python-dotenv

## Estructura

```text
api.py                         Punto de entrada de Flask y Swagger

db/database.py                 Pool de conexiones PostgreSQL
models/                        Acceso a datos
  estudiantes/estudiantes.py
  incripciones/inscripciones.py
nspace/                         Namespaces y endpoints HTTP
  auth/auth.py                  Login y emision de JWT
  estudiantes/estudiantes.py   Endpoints de estudiantes
  incripciones/inscripciones.py Endpoints de inscripciones
requirements.txt               Dependencias Python
.env                            Configuracion local, ignorada por Git
```

## Requisitos

- Python instalado
- PostgreSQL 18 o compatible
- Base de datos `Sistema de Cursos Online`
- Tablas y relaciones del esquema de cursos creadas en PostgreSQL

Las credenciales se configuran en `.env`. Ese archivo no debe subirse al repositorio.

Variables esperadas:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Sistema de Cursos Online
DB_USER=postgres
DB_PASSWORD=tu_password_local
DB_POOL_MIN=1
DB_POOL_MAX=5
DB_CONNECT_TIMEOUT=5
JWT_SECRET_KEY=tu_clave_secreta
```

## Instalacion

Desde la raiz del proyecto:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecucion

Asegura primero que PostgreSQL este ejecutandose. Luego:

```powershell
.\venv\Scripts\python.exe api.py
```

La API queda disponible en:

- Swagger UI: http://127.0.0.1:5000/
- Especificacion OpenAPI: http://127.0.0.1:5000/swagger.json

## Autenticacion

El login se realiza en `POST /auth/login`:

```json
{
  "username": "usuario",
  "password": "password"
}
```

La respuesta contiene un `access_token`. En Swagger se usa desde **Authorize** con el formato:

```text
Bearer <access_token>
```

Las operaciones de escritura de estudiantes requieren JWT:

- `POST /estudiantes/`
- `PUT /estudiantes/{idestudiante}`
- `DELETE /estudiantes/{idestudiante}`

El token incluye el identificador del usuario y su rol. La comprobacion detallada de permisos por rol debe mantenerse en los endpoints administrativos.

## Endpoints actuales

### Estudiantes

- `GET /estudiantes/`
- `GET /estudiantes/{idestudiante}`
- `POST /estudiantes/`
- `PUT /estudiantes/{idestudiante}`
- `DELETE /estudiantes/{idestudiante}`

### Inscripciones

- `GET /inscripciones/`
- `GET /inscripciones/{idinscripcion}`
- `POST /inscripciones/`
- `PUT /inscripciones/{idinscripcion}`
- `DELETE /inscripciones/{idinscripcion}`

### Autenticacion

- `POST /auth/login`

## Base de datos

La aplicacion usa `ThreadedConnectionPool`. El pool se crea de forma perezosa en la primera consulta, usa entre 1 y 5 conexiones por defecto y devuelve las conexiones despues de cada operacion.

El esquema actual incluye, entre otras, las tablas `usuarios`, `estudiantes`, `cursos`, `inscripciones`, `permisos` y `sesiones`.

Las contrasenas de `usuarios` deben almacenarse como hashes bcrypt. Nunca guardes contrasenas ni tokens reales en el repositorio.

## Plan de despliegue en AWS

La API esta preparada para migrar a una arquitectura AWS de bajo coste, sujeta a la elegibilidad y a los limites vigentes del AWS Free Tier:

```text
Cliente
  |
  v
EC2: Flask + Gunicorn + Nginx opcional
  |
  v
RDS PostgreSQL: base de datos privada
```

### EC2

- Ejecuta la API con Gunicorn y un servicio `systemd`.
- Usa un Security Group que permita HTTP/HTTPS y SSH solo desde una IP administrativa.
- Configura las variables de entorno fuera del repositorio.
- Ajusta `DB_POOL_MIN` y `DB_POOL_MAX` a valores bajos para una instancia pequena.
- No uses el servidor de desarrollo de Flask en produccion.

### RDS PostgreSQL

- Migra aqui el esquema y los datos de `Sistema de Cursos Online`.
- Mantén RDS en una red privada cuando sea posible.
- Permite el puerto 5432 unicamente desde el Security Group de EC2.
- No expongas PostgreSQL directamente a Internet.
- Configura backups y monitorea el consumo para evitar cargos inesperados.

### S3

S3 no es necesario para las operaciones actuales porque la API no gestiona archivos. Se puede agregar para:

- Archivos de cursos o recursos descargables.
- Backups exportados.
- Logs o documentos generados.

La instancia EC2 debería usar un IAM Role para acceder a S3, sin guardar access keys en `.env`.

### CloudFront

CloudFront tampoco es necesario para la primera version de esta API. Tiene sentido cuando exista:

- Un frontend o contenido estatico que distribuir.
- Archivos almacenados en S3.
- Una necesidad real de cache, HTTPS en el borde o distribucion geografica.

Para comenzar, EC2 con Nginx y HTTPS puede ser suficiente. Agrega CloudFront despues de medir la necesidad y revisar sus costes.

### Configuracion de produccion

En AWS no copies el `.env` local con credenciales reales al repositorio. Usa variables de entorno del servicio, AWS Systems Manager Parameter Store o un gestor de secretos. La clave JWT debe ser diferente de la local y nunca debe aparecer en logs.

Antes de publicar:

1. Cambiar `debug=True` por una configuracion de produccion.
2. Ejecutar Flask mediante Gunicorn.
3. Restringir Security Groups.
4. Configurar HTTPS.
5. Probar la conexion contra RDS y el pool con limites pequenos.
6. Verificar el presupuesto y las alertas de costes de AWS.

## Flujo de trabajo Git

Trabaja en ramas de funcionalidad y abre un Pull Request hacia `main`:

```powershell
git switch -c nombre-de-la-funcionalidad
git add .
git commit -m "Descripcion del cambio"
git push -u origin nombre-de-la-funcionalidad
```

Despues del merge en GitHub:

```powershell
git switch main
git pull origin main
```

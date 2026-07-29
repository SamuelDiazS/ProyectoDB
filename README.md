# ProyectoDB

Esta aplicación FastAPI usa `asyncpg` para conectarse a una base de datos PostgreSQL y renderiza plantillas con Jinja2.

## Despliegue en Vercel

1. Añade la variable de entorno `DATABASE_URL` en el dashboard de Vercel.
2. Asegúrate de que el valor sea una URL de conexión PostgreSQL válida.
3. Despliega el proyecto desde el repositorio.

## Estructura para Vercel

- `vercel.json`: configura la ruta de la API a `api/index.py`.
- `api/index.py`: punto de entrada ASGI para Vercel.
- `api/requirements.txt`: dependencias instaladas para el despliegue.

## Variables de entorno

- `DATABASE_URL`: URL de conexión PostgreSQL.

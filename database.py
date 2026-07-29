import os
from typing import AsyncGenerator

from loguru import logger

import asyncpg

# Configuración de la URL de la base de datos mediante variable de entorno.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://estudiantes:npg_FtxeYOVU8yD7@ep-withered-wind-apq7hmfj-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
)
# Variable global para almacenar el pool de conexiones
_pool: asyncpg.Pool | None = None



async def init_db_pool():
    """Inicializa el pool de conexiones."""
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=10,  # Conexiones mínimas que se mantendrán abiertas
                max_size=20,  # Conexiones máximas permitidas simultáneamente
                max_queries=50000,  # Reinicia la conexión tras X consultas para liberar memoria
                max_inactive_connection_lifetime=300.0,  # Tiempo en segundos antes de cerrar conexiones inactivas
            )
            logger.info("Connection pool con PostgreSQL creado exitosamente.")
        except Exception as e:
            logger.error(f"Error al crear el connection pool: {e}")
            raise e


async def close_db_pool():
    """Cierra el pool de conexiones limpiamente."""
    global _pool
    if _pool is not None:
        await _pool.close()
        logger.info("Connection pool con PostgreSQL cerrado.")


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependencia para FastAPI.
    Adquiere una conexión del pool y la devuelve.
    Garantiza que la conexión se libere (regrese al pool) al terminar el request.
    """
    if _pool is None:
        raise RuntimeError("El pool de conexiones no ha sido inicializado.")

    # Adquiere una conexión del pool de forma asíncrona
    async with _pool.acquire() as connection:
        yield connection
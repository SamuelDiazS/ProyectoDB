import asyncpg
from fastapi import HTTPException
from loguru import logger

async def todos_los_autores(db: asyncpg.Connection):
    try:
        query = "SELECT * FROM autores;"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("No se pudo consultar la base de datos")
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )

async def autores_por_parametros(db: asyncpg.Connection, año_nacimiento: int, pais: str):
    try:
        query = "SELECT * FROM autores WHERE nacimiento = $1 AND pais = $2;"
        rows = await db.fetch(query, año_nacimiento, pais)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("No se pudo consultar la base de datos")
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )
        
async def promedio_puntuacion_libros(db: asyncpg.Connection, titulo: str, formato: str):
    try:
        query = "SELECT titulo, formato FROM lista_larga WHERE formato != 'hardcover' LIMIT 10;"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("No se pudo consultar la base de datos")
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )

async def listar_titulo_autor(db: asyncpg.Connection):
    try:
        query = "SELECT titulo, autor FROM lista_larga ORDER BY titulo;"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("No se pudo consultar la base de datos")
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )

async def top10_titulo_puntuacion(db: asyncpg.Connection):
    try:
        query = "SELECT titulo, puntuacion FROM lista_larga ORDER BY puntuacion DESC LIMIT 10;"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("No se pudo consultar la base de datos")
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )


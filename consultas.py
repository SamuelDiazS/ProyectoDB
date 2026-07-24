import asyncpg
from fastapi import Depends, HTTPException
from loguru import logger
from database import get_db
async def autores(db: asyncpg.Connection = Depends(get_db)):
    """
    Endpoint concurrente. `db` es una conexión lista para usar
    tomada eficientemente del pool.
    """
    try:
        query = "SELECT * FROM autores LIMIT 10;"
        rows = await db.fetch(query)
        logger.info("ingreso a consultas")
        registros = [dict(row) for row in rows]
        logger.debug(f"los usuarios son: {registros}")
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )

async def traer_titulos(db: asyncpg.connection = Depends(get_db)):
    try:
        query = "SELECT titulos FROM autores LITMIT 10"
        rows = await db.fetch(query)
        logger.info("titulos hacia mi")
        titulos = [dict(rows) for row in rows]
        logger.debug(f"los titulos son {titulos}")
        return titulos
    except Exception as i:
        raise HTTPException(
            status_code=500, detail=f"Error de base de datos (titulos): {str(i)}"
        )
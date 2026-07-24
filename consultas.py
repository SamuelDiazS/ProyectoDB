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

async def traer_titulos(db: asyncpg.Connection = Depends(get_db)):
    try:
        query = "SELECT titulo FROM lista_larga;"
        rows = await db.fetch(query)
        logger.info("consulta de titulos")
        registros = [dict(row) for row in rows]
        logger.debug(f"los titulos son: {registros}")
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )

async def traer_anios(db: asyncpg.Connection = Depends(get_db)):
    try:
        query = "SELECT titulo, autor FROM lista_larga WHERE anio = 2023"
        rows = await db.fetch(query)
        logger.info("ingreso a consultas - titulos")
        registros = [dict(row) for row in rows]
        logger.debug(f"los datos son son: {registros}")
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}"
        )
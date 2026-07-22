from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from database import close_db_pool, get_db, init_db_pool
from consultas import autores


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio: creamos el pool
    await init_db_pool()
    yield
    # Evento de apagado: cerramos el pool
    await close_db_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/usuarios")
async def listar_usuarios(datos=Depends(autores)):
    """
    Endpoint concurrente. `datos` proviene de una conexión lista
    para usar tomada eficientemente del pool.
    """
    return datos
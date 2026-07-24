from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates

from database import close_db_pool, get_db, init_db_pool
from consultas import autores, traer_titulos, traer_anios


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio: creamos el pool
    await init_db_pool()
    yield
    # Evento de apagado: cerramos el pool
    await close_db_pool()


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


@app.get("/usuarios")
async def listar_usuarios(request: Request, datos=Depends(autores)):
    """
    Endpoint concurrente. `datos` proviene de una conexión lista
    para usar tomada eficientemente del pool.
    Renderiza el diccionario de resultados directamente en una
    tabla HTML sin estilos.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"registros":datos}
    )

@app.get("/titulo")
async def traer_titulo(datos=Depends(traer_titulos)):
    return datos

@app.get("/anio")
async def traer_anio(datos=Depends(traer_anios)):
    return datos
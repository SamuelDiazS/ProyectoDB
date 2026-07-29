from pathlib import Path
from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from contextlib import asynccontextmanager
from typing import Annotated
import asyncpg
from loguru import logger

from consultas import (
    todos_los_autores,
    autores_por_parametros,
    promedio_puntuacion_libros,
    listar_titulo_autor,
    top10_titulo_puntuacion,
)
from database import init_db_pool, close_db_pool, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield
    await close_db_pool()

app = FastAPI(lifespan=lifespan)
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/autores")
async def listar_usuarios(db: asyncpg.Connection = Depends(get_db)):
    datos = await todos_los_autores(db)
    return datos

@app.get("/autores1")
async def listar(
    request: Request,
    db: Annotated[asyncpg.Connection, Depends(get_db)],
    year: int | None = None,
    pais: str | None = None,
):
    if year is None and pais is None:
        datos = await todos_los_autores(db)
    else:
        datos = await autores_por_parametros(db, year, pais)
    return datos

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/lista-larga/html")
async def listar_titulo_autor_html(
    request: Request,
    db: Annotated[asyncpg.Connection, Depends(get_db)],
    titulo: str | None = None,
    autor: str | None = None,
):
    datos = await listar_titulo_autor(db)

    if titulo:
        filtro_titulo = titulo.strip().lower()
        datos = [
            libro for libro in datos
            if filtro_titulo in str(libro.get("titulo", "")).lower()
        ]

    if autor:
        filtro_autor = autor.strip().lower()
        datos = [
            libro for libro in datos
            if filtro_autor in str(libro.get("autor", "")).lower()
        ]

    return templates.TemplateResponse(
        request=request,
        name="respuesta.html",
        context={"autores": [], "libros": datos, "mejores": [], "titulo": titulo or "", "autor": autor or ""},
    )

@app.get("/autores/html")
async def listar_autores_html(
    request: Request,
    db: Annotated[asyncpg.Connection, Depends(get_db)],
    year: int | None = None,
    pais: str | None = None,
):
    logger.info(f"Parametros recibidos: year={year}, pais={pais}")
    if year is None and pais is None:
        datos = await todos_los_autores(db)
    else:
        datos = await autores_por_parametros(db, year, pais)
    return templates.TemplateResponse(request=request, name="respuesta.html", context={"autores": datos, "libros": [], "mejores": []})

@app.get("/top10/html")
async def top10_libros_html(
    request: Request,
    db: Annotated[asyncpg.Connection, Depends(get_db)],
):
    datos = await top10_titulo_puntuacion(db)
    return templates.TemplateResponse(
        request=request,
        name="respuesta.html",
        context={"autores": [], "libros": [], "mejores": datos},
    )

@app.get("/dura")
async def listar_autores_html(
    request: Request,
    db: Annotated[asyncpg.Connection, Depends(get_db)],
    titulo: str | None = None,
    formato: str | None = None,
):
    datos = await promedio_puntuacion_libros(db, titulo, formato)
    return templates.TemplateResponse(
        request=request,
        name="respuesta.html",
        context={"autores": [], "libros": datos, "mejores": [], "titulo": titulo or "", "formato": formato or ""},
    )

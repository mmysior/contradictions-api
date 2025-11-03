import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router

from .core.config import settings
from .core.logging import setup_logging
from .core.vectors import get_vector_store

PROJECT_NAME = settings.PROJECT_NAME
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME}")
    logger.info(f"API version: {settings.API_V1_STR}")
    logger.info("Initializing vector store and computing embeddings...")
    get_vector_store()
    logger.info("Vector store initialized successfully")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
def read_root():
    return "Server is running."

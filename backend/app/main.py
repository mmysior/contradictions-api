from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router

from .core.config import settings

PROJECT_NAME = settings.PROJECT_NAME


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
def read_root():
    return "Server is running."

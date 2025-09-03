from fastapi import APIRouter

from app.api.routes.contradictions import router as contradictions_router
from app.api.routes.parameters import router as parameters_router
from app.api.routes.patents import router as patents_router
from app.api.routes.principles import router as principles_router
from app.api.routes.utils import router as utils_router

api_router = APIRouter()
api_router.include_router(utils_router, tags=["utils"])
api_router.include_router(principles_router, tags=["principles"])
api_router.include_router(parameters_router, tags=["parameters"])
api_router.include_router(contradictions_router, tags=["contradictions"])
api_router.include_router(patents_router, tags=["patents"])

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)

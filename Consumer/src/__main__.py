from collections.abc import Callable
import uvicorn  # type: ignore
from fastapi import (
    FastAPI,
    Request,
    Response,
)
from loguru import logger
from src.routers.person_router import person_router
from src.routers.educational_institution_router import educational_institution_router
from src.routers.test_institution_router import test_institution_router
from src.routers.test_router import test_result_router
from src.routers.health_check import health_check_router

fastapi_app = FastAPI()


fastapi_app.include_router(
    person_router,
    tags=["person"]
)
fastapi_app.include_router(
    educational_institution_router,
    tags=["e_i"]
)
fastapi_app.include_router(
    test_institution_router,
    tags=["t_i"]
)
fastapi_app.include_router(
    test_result_router,
    tags=["test_result"]
)
fastapi_app.include_router(
    health_check_router,
    tags=["health_check"]
)


@fastapi_app.middleware("http")
async def log_middle(request: Request, call_next: Callable) -> Response:
    url = "/" + str(request.url).removeprefix(str(request.base_url))
    logger.info(f"Request: {request.method} {url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} {url}")
    return response


def run() -> None:
    uvicorn.run(
        "src.__main__:fastapi_app",
        host="0.0.0.0", 
        port=8082,  
        loop="uvloop",
    )


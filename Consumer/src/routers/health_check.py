from fastapi import APIRouter


health_check_router = APIRouter()


@health_check_router.get("/health_check")
def check_health() -> str:
    return "Consumer is healthy"
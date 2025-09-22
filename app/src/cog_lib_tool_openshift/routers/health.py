import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

health_router = APIRouter(tags=["health"], prefix="/health")


# Configure test endpoint
@health_router.get("/test", operation_id="Test_health", status_code=200)
def test_endpoint() -> str:
    logger.debug("Testing endpoint")
    return "OK"

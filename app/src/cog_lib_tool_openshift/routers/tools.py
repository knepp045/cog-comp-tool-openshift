from fastapi import APIRouter, Depends

from ..auth import get_api_key
from ..tools.openshift import list_namespaces

tools_router = APIRouter(tags=["tools"], prefix="/tools")


@tools_router.get(
    "/namespaces",
    operation_id="List OpenShift namespaces",
    status_code=200,
)
def get_namespaces(token: str = Depends(get_api_key)) -> dict:
    """Return the available OpenShift namespaces for the authenticated user."""

    return list_namespaces(token)

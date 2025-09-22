from fastapi import APIRouter, Depends

from cog_lib_tool_atlassian.auth import get_api_key
from cog_lib_tool_atlassian.tools.bitbucket import search_code

tools_router = APIRouter(tags=["tools"], prefix="/tools")


@tools_router.post(
    "/search", operation_id="Search Bitbucket code", status_code=200
)
def search(query: str, token: str = Depends(get_api_key)) -> dict:
    """Search Bitbucket for code snippets."""
    return search_code(query, token)

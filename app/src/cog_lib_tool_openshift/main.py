import logging

from cog_lib_tool_atlassian.routers.health import health_router
from cog_lib_tool_atlassian.routers.oauth import oauth_router
from cog_lib_tool_atlassian.routers.tools import tools_router
from cog_lib_tool_atlassian.settings import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, RouteType
# Configure logger
settings = get_settings()
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)-8s %(asctime)s - %(message)s",
    level=settings.log_level,
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Create app
app = FastAPI(
    title=settings.app_name,
    version="1.0",
    description=settings.description,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(tools_router)
app.include_router(health_router)
app.include_router(oauth_router)

# Generate an MCP server directly from the FastAPI app
httpmethods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
custom_maps = [
    RouteMap(methods=httpmethods, pattern=r"^/tools/.*", route_type=RouteType.TOOL),
    RouteMap(methods=httpmethods, pattern=r"^/.*", route_type=RouteType.IGNORE),
]

mcp_server = FastMCP.from_fastapi(app)
mcp_app = mcp_server.sse_app()
app.mount("/", mcp_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

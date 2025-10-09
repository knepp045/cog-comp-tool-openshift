import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from fastmcp.server.openapi import MCPType, RouteMap

# server.py
from cog_lib_tool_openshift.routers.health import health_router
from cog_lib_tool_openshift.routers.oauth import oauth_router
from cog_lib_tool_openshift.routers.tools import tools_router
from cog_lib_tool_openshift.settings import get_settings

# Configure logger and get settings
settings = get_settings()
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)-8s %(asctime)s - %(message)s",
    level=settings.log_level,
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Create a FastAPI (REST) app
rest_app = FastAPI(
    title=settings.app_name,
    version="1.0",
    description=settings.description,
)
rest_app.include_router(tools_router)
rest_app.include_router(health_router)
rest_app.include_router(oauth_router)

# Generate an MCP app from the FastAPI app
httpmethods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
custom_maps = [
    RouteMap(methods=httpmethods, pattern=r"^/tools/.*", mcp_type=MCPType.TOOL),
    RouteMap(methods=httpmethods, pattern=r".*", mcp_type=MCPType.EXCLUDE),
]

mcp_server = FastMCP.from_fastapi(
    rest_app,
    route_maps=custom_maps,
    # auth=auth
)
mcp_app = mcp_server.http_app()

# Create outer app that wraps both, use MCP server lifespan
routes = [*mcp_app.routes, *rest_app.routes]
app = FastAPI(
    routes=routes,
    lifespan=mcp_app.lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    body = await request.body()  # Read the raw body (bytes)
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Raw body: {body.decode('utf-8', errors='ignore')}")
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

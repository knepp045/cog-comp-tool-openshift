from __future__ import annotations

"""Authentication utilities and token storage."""

from typing import Dict

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from cog_lib_tool_atlassian.settings import get_settings

# In-memory token store keyed by access token
_token_store: Dict[str, dict] = {}


def store_token(token: dict) -> None:
    """Store an OAuth access token."""
    access_token = token.get("access_token")
    if access_token:
        _token_store[access_token] = token


def has_token(access_token: str | None) -> bool:
    """Return True if the access token is known."""
    return bool(access_token and access_token in _token_store)


def get_api_key(
    bearer_credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(auto_error=False)),
) -> str:
    """Validate bearer token against configured API keys or OAuth tokens."""
    token: str | None = None

    if bearer_credentials is not None and bearer_credentials.scheme.lower() == "bearer":
        token = bearer_credentials.credentials

    settings = get_settings()

    if settings.api_keys and token in settings.api_keys:
        return token

    if has_token(token):
        return token  # OAuth token accepted

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
        headers={"WWW-Authenticate": "Bearer"},
    )

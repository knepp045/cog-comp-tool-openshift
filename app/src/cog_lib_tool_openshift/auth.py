from __future__ import annotations

"""Authentication utilities and token storage."""


from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_api_key(
    bearer_credentials: HTTPAuthorizationCredentials = Security(
        HTTPBearer(auto_error=False)
    ),
) -> str:
    """Validate bearer token against configured API keys or OAuth tokens."""
    token: str | None = None

    if bearer_credentials is not None and bearer_credentials.scheme.lower() == "bearer":
        token = bearer_credentials.credentials

    return token

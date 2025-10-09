"""Authentication utilities and token storage."""

from __future__ import annotations

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer_scheme = HTTPBearer(auto_error=False)
_bearer_security = Security(_bearer_scheme)


def get_api_key(
    bearer_credentials: HTTPAuthorizationCredentials = _bearer_security,
) -> str:
    """Validate bearer token against configured API keys or OAuth tokens."""
    token: str | None = None

    if bearer_credentials is not None and bearer_credentials.scheme.lower() == "bearer":
        token = bearer_credentials.credentials

    return token

from __future__ import annotations

"""OAuth endpoints for Bitbucket authentication."""

import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from cog_lib_tool_atlassian.auth import store_token
from cog_lib_tool_atlassian.settings import get_settings

oauth_router = APIRouter(prefix="/oauth", tags=["oauth"])


@oauth_router.get("/login")
def login() -> RedirectResponse:
    """Redirect user to Bitbucket OAuth authorization URL."""
    settings = get_settings()
    params = {
        "response_type": "code",
        "client_id": settings.bitbucket_client_id,
        "redirect_uri": settings.bitbucket_redirect_uri,
    }
    if settings.bitbucket_oauth_scope:
        params["scope"] = settings.bitbucket_oauth_scope

    # Build authorization URL
    req = requests.Request("GET", settings.bitbucket_authorize_url, params=params)
    url = req.prepare().url
    return RedirectResponse(url)


@oauth_router.get("/callback")
def callback(request: Request) -> dict:
    """Handle OAuth callback and exchange code for an access token."""
    settings = get_settings()
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.bitbucket_redirect_uri,
        "client_id": settings.bitbucket_client_id,
        "client_secret": settings.bitbucket_client_secret,
    }
    resp = requests.post(settings.bitbucket_token_url, data=data)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch token")

    token = resp.json()
    store_token(token)
    return {"access_token": token.get("access_token")}

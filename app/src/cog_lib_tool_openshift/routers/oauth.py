from __future__ import annotations

"""OAuth endpoints for OpenShift authentication."""

import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from ..auth import store_token
from ..settings import get_settings

oauth_router = APIRouter(prefix="/oauth", tags=["oauth"])


@oauth_router.get("/login")
def login() -> RedirectResponse:
    """Redirect user to the configured OpenShift OAuth authorization URL."""
    settings = get_settings()
    if not (
        settings.openshift_authorize_url
        and settings.openshift_client_id
        and settings.openshift_redirect_uri
    ):
        raise HTTPException(status_code=500, detail="OpenShift OAuth is not configured")

    params = {
        "response_type": "code",
        "client_id": settings.openshift_client_id,
        "redirect_uri": settings.openshift_redirect_uri,
    }
    if settings.openshift_oauth_scope:
        params["scope"] = settings.openshift_oauth_scope

    # Build authorization URL
    req = requests.Request("GET", settings.openshift_authorize_url, params=params)
    url = req.prepare().url
    return RedirectResponse(url)


@oauth_router.get("/callback")
def callback(request: Request) -> dict:
    """Handle OAuth callback and exchange code for an access token."""
    settings = get_settings()
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    if not (
        settings.openshift_token_url
        and settings.openshift_redirect_uri
        and settings.openshift_client_id
    ):
        raise HTTPException(status_code=500, detail="OpenShift OAuth is not configured")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.openshift_redirect_uri,
        "client_id": settings.openshift_client_id,
        "client_secret": settings.openshift_client_secret,
    }
    verify = settings.openshift_ca_bundle or settings.openshift_verify_ssl
    resp = requests.post(settings.openshift_token_url, data=data, verify=verify)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch token")

    token = resp.json()
    store_token(token)
    return {"access_token": token.get("access_token")}

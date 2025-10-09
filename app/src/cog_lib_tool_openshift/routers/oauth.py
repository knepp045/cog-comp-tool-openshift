from __future__ import annotations

from urllib.parse import urlencode, urljoin

import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from cog_lib_tool_openshift.settings import get_settings

oauth_router = APIRouter(prefix="/oauth", tags=["oauth"])

AUTHORIZE_PATH = "/oauth/authorize"
TOKEN_PATH = "/oauth/token"


def _join_url(base_url: str | None, path: str) -> str:
    normalized_base = base_url.rstrip("/") + "/"
    normalized_path = path.lstrip("/")
    return urljoin(normalized_base, normalized_path)


def _tool_url(path: str) -> str:
    settings = get_settings()
    return _join_url(settings.base_url, path)


@oauth_router.get("/login")
def login() -> RedirectResponse:
    """Redirect user to the configured OpenShift OAuth authorization URL."""
    settings = get_settings()
    if not (
        settings.openshift_oauth_url and settings.openshift_client_id and settings.base_url
    ):
        raise HTTPException(status_code=500, detail="OpenShift OAuth is not configured")

    redirect_uri = _tool_url("/oauth/callback")

    params = {
        "response_type": "code",
        "client_id": settings.openshift_client_id,
        "redirect_uri": redirect_uri,
    }
    if settings.openshift_oauth_scope:
        params["scope"] = settings.openshift_oauth_scope

    # Build authorization URL
    authorize_url = _join_url(
        settings.openshift_oauth_url,
        AUTHORIZE_PATH
    )
    req = requests.Request("GET", authorize_url, params=params)
    url = req.prepare().url
    return RedirectResponse(url)


@oauth_router.get("/callback")
def callback(request: Request):
    """Handle OAuth callback and exchange code for an access token."""
    settings = get_settings()
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    if not (
        settings.openshift_oauth_url
        and settings.openshift_client_id
        and settings.base_url
        and settings.assistant_base_url
    ):
        raise HTTPException(status_code=500, detail="OpenShift OAuth is not configured")

    redirect_uri = _tool_url("/oauth/callback")
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": settings.openshift_client_id,
        "client_secret": settings.openshift_client_secret,
    }

    verify = settings.openshift_ca_bundle or settings.openshift_verify_ssl
    token_url = _join_url(
        settings.openshift_oauth_url,
        TOKEN_PATH
    )
    resp = requests.post(token_url, data=data, verify=verify)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code, detail=f"Failed to fetch token:{data} {resp.content}"
        )

    token = resp.json()["access_token"]

    # Safely encode query parameters
    query = urlencode({"server": "openshift", "token": token})

    redirect_url = (
        f"{_join_url(settings.assistant_base_url, '/store-token')}"
        f"?{query}"
    )

    return RedirectResponse(url=redirect_url)

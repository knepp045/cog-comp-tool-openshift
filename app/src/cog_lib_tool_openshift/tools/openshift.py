"""Helpers for interacting with the OpenShift API."""

from __future__ import annotations

import logging
from urllib.parse import urljoin

import requests

from cog_lib_tool_openshift.settings import get_settings

logger = logging.getLogger(__name__)


def _build_api_url(*parts: str) -> str:
    settings = get_settings()
    base_url = settings.openshift_api_url.rstrip("/")
    suffix = "/".join(part.strip("/") for part in parts if part)
    return f"{base_url}/{suffix}" if suffix else base_url


def list_namespaces(token: str) -> dict:
    """Return the namespaces the authenticated user can list."""

    logger.info("Executing list_namespaces")
    logger.info(f"Token: {token}")

    settings = get_settings()
    url = _build_api_url("apis", "project.openshift.io", "v1", "projects")
    headers = {"Authorization": f"Bearer {token}"}
    if settings.openshift_ca_bundle:
        verify = settings.openshift_ca_bundle
    else:
        verify = settings.openshift_verify_ssl

    response = requests.get(url, headers=headers, verify=verify)
    if response.status_code == 401:
        login_url = urljoin((settings.base_url or "").rstrip("/") + "/", "oauth/login")
        return {
            "error": f"Not logged in, point the user to {login_url}"
        }
    payload = response.json()
    items = payload.get("items", [])
    namespaces = [
        item.get("metadata", {}).get("name")
        for item in items
        if item.get("metadata", {}).get("name")
    ]
    return {"namespaces": namespaces, "raw": payload}

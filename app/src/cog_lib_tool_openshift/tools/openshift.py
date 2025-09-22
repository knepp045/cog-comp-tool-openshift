"""Helpers for interacting with the OpenShift API."""

from __future__ import annotations

import requests

from ..settings import get_settings


def _build_api_url(*parts: str) -> str:
    settings = get_settings()
    base_url = settings.openshift_api_url.rstrip("/")
    suffix = "/".join(part.strip("/") for part in parts if part)
    return f"{base_url}/{suffix}" if suffix else base_url


def list_namespaces(token: str) -> dict:
    """Return the namespaces the authenticated user can list."""

    settings = get_settings()
    url = _build_api_url("api", "v1", "namespaces")
    headers = {"Authorization": f"Bearer {token}"}
    if settings.openshift_ca_bundle:
        verify = settings.openshift_ca_bundle
    else:
        verify = settings.openshift_verify_ssl

    response = requests.get(url, headers=headers, verify=verify)
    response.raise_for_status()
    payload = response.json()
    items = payload.get("items", [])
    namespaces = [item.get("metadata", {}).get("name") for item in items if item.get("metadata", {}).get("name")]
    return {"namespaces": namespaces, "raw": payload}

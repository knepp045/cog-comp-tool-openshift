import requests

from cog_lib_tool_atlassian.settings import get_settings


def search_code(query: str, token: str) -> dict:
    """Search Bitbucket for code snippets using the provided OAuth token."""
    settings = get_settings()
    url = f"{settings.bitbucket_host}/rest/api/latest/search/code"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"searchTerm": query}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()

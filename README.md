# Description
MCP toolserver exposing OpenShift automation utilities.

# Settings
See `app/src/cog_lib_tool_openshift/settings.py` for the supported configuration parameters. You can change the default values in the settings module, create an `.env` file or override them using environment variables.

## OAuth with OpenShift
The server can authenticate users via an OpenShift cluster. Configure the following environment variables (or `.env` values):

- `BASE_URL`: Public base URL of this tool (for example `https://tool.example.com/oauth`).
- `ASSISTANT_BASE_URL`: Base URL of the assistant that stores OAuth tokens, without the `/store_token` suffix.
- `OPENSHIFT_CLIENT_ID`
- `OPENSHIFT_CLIENT_SECRET`
- `OPENSHIFT_OAUTH_URL`: Base URL of the OpenShift OAuth server (for example `https://oauth-openshift.apps.cluster.example.com`). The tool automatically appends `/oauth/authorize` and `/oauth/token` to this base URL when communicating with the cluster.
- `OPENSHIFT_OAUTH_SCOPE` *(optional)*

Provide the cluster API endpoint via `OPENSHIFT_API_URL`. Optionally set `OPENSHIFT_CA_BUNDLE` to the path of a CA bundle that should be trusted when contacting the cluster. If omitted, TLS verification can be toggled with `OPENSHIFT_VERIFY_SSL` (defaults to `true`).

Once configured, users can visit `${BASE_URL}/login` to start the authorization flow. OpenShift redirects back to `${BASE_URL}/callback`, where the tool exchanges the authorization code for a token and finally redirects to `${ASSISTANT_BASE_URL}/store_token` with the newly issued access token.

# OpenShift namespace listing
The `/tools/namespaces` endpoint returns the namespaces visible to the authenticated user. A valid OAuth token or API key must be provided to access this tool. The response contains the extracted namespace names as well as the raw Kubernetes API payload for convenience.

# Run locally
- Install packages
  - `uv pip install -e .`
- Install FastAPI extras (for local development)
  - `uv pip install fastapi[standard]`
- Run the server
  - `fastapi run app/src/cog_lib_tool_openshift/main.py`

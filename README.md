# Description
MCP toolserver exposing OpenShift automation utilities.

# Settings
See `app/src/cog_lib_tool_openshift/settings.py` for the supported configuration parameters. You can change the default values in the settings module, create an `.env` file or override them using environment variables.

## OAuth with OpenShift
The server can authenticate users via an OpenShift cluster. Configure the following environment variables (or `.env` values):

- `OPENSHIFT_CLIENT_ID`
- `OPENSHIFT_CLIENT_SECRET`
- `OPENSHIFT_AUTHORIZE_URL`
- `OPENSHIFT_TOKEN_URL`
- `OPENSHIFT_REDIRECT_URI`
- `OPENSHIFT_OAUTH_SCOPE` *(optional)*

Provide the cluster API endpoint via `OPENSHIFT_API_URL`. Optionally set `OPENSHIFT_CA_BUNDLE` to the path of a CA bundle that should be trusted when contacting the cluster. If omitted, TLS verification can be toggled with `OPENSHIFT_VERIFY_SSL` (defaults to `true`).

Once configured, users can visit `/oauth/login` to start the authorization flow. After approving access, an access token is stored for use with the tools.

# OpenShift namespace listing
The `/tools/namespaces` endpoint returns the namespaces visible to the authenticated user. A valid OAuth token or API key must be provided to access this tool. The response contains the extracted namespace names as well as the raw Kubernetes API payload for convenience.

# Run locally
- Install packages
  - `uv pip install -e .`
- Install FastAPI extras (for local development)
  - `uv pip install fastapi[standard]`
- Run the server
  - `fastapi run app/src/cog_lib_tool_openshift/main.py`

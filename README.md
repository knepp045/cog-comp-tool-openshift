# Description
MCP toolserver for interactions with Atlassian Server tools

# Settings
cog_lib_tool_afko
See `app/src/cog_lib_tool_afko/settings.py` for which parameters you can set.
You can change the default values in the config, create an `.env` file or override them using environment variables.

## OAuth with Bitbucket
The server can authenticate users via Bitbucket's OAuth provider. Configure the following environment variables (or `.env` values):

- `BITBUCKET_CLIENT_ID`
- `BITBUCKET_CLIENT_SECRET`
- `BITBUCKET_AUTHORIZE_URL`
- `BITBUCKET_TOKEN_URL`
- `BITBUCKET_REDIRECT_URI`
- `BITBUCKET_HOST`

Once configured, users can visit `/oauth/login` to start the authorization flow. After approving access, an access token is stored for use with the tools.

# Bitbucket code search
The `/tools/search` endpoint allows searching Bitbucket repositories for code snippets. A valid OAuth token or API key must be provided to access this tool.

# Run locally
- Install packages
  - `uv pip install -e .`
- Install full fastapi
  - `uv pip install fastapi[standard]
- Run the server
  - `fastapi run /path/to/main.py

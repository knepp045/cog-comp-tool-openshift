import logging
from functools import lru_cache
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Default values for settings object,
    if none presented they are obligated to overwrite, environment variables
    will overwrite default values as stated below
    """

    # App settings
    app_name: str = "cog-openshift"
    description: str = "Expose MCP tools backed by OpenShift APIs"

    # CORS
    cors_allow_origins: tuple = ("*",)  # only accessible through local network anyway

    # Authentication settings
    # Strings can behave as lists be careful when change types below!
    api_keys: tuple[str, ...] | None = None
    authorized_groups: tuple[str, ...] | None = None

    # OAuth configuration for OpenShift
    openshift_client_id: str | None = None
    openshift_client_secret: str | None = None
    openshift_authorize_url: str | None = None
    openshift_token_url: str | None = None
    openshift_redirect_uri: str | None = None
    openshift_oauth_scope: str | None = None

    # OpenShift API
    openshift_api_url: str = "https://openshift.default.svc"
    openshift_verify_ssl: bool = True
    openshift_ca_bundle: str | None = None

    # logging
    log_level: int = logging.INFO  # 20: info, 10: debug

    @model_validator(mode="after")  # type: ignore
    def configure_auth(cls, m: Self) -> Self:
        """
        Validator to make sure at least one authentication method is configured
        """
        if not (
            m.api_keys
            or m.authorized_groups
            or (m.openshift_client_id and m.openshift_client_secret)
        ):
            raise ValueError(
                "You have to configure an api key, authorized groups or OAuth credentials"
            )

        if m.openshift_client_id and not (
            m.openshift_authorize_url
            and m.openshift_token_url
            and m.openshift_redirect_uri
        ):
            raise ValueError(
                "OpenShift OAuth requires authorize, token and redirect URLs to be configured"
            )

        if not m.openshift_api_url:
            raise ValueError("The OpenShift API URL must be configured")

        return m

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

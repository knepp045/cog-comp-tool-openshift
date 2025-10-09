import logging
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

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
    base_url: str | None = None
    assistant_base_url: str | None = None
    openshift_client_id: str | None = None
    openshift_client_secret: str | None = None
    openshift_oauth_url: str | None = None
    openshift_oauth_scope: str | None = None

    # OpenShift API
    openshift_api_url: str = "https://openshift.default.svc"
    openshift_verify_ssl: bool = True
    openshift_ca_bundle: str | None = None

    # logging
    log_level: int = logging.INFO  # 20: info, 10: debug

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

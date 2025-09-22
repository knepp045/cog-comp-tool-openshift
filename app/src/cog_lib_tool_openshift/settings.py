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
    app_name: str = "afko"
    description: str = "Retrieves the meaning of acronyms"

    # CORS
    cors_allow_origins: tuple = ("*",)  # only accessible through local network anyway

    # Authentication settings
    # Strings can behave as lists be careful when change types below!
    api_keys: tuple[str, ...] | None = None
    authorized_groups: tuple[str, ...] | None = None

    # OAuth configuration for Bitbucket
    bitbucket_client_id: str | None = None
    bitbucket_client_secret: str | None = None
    bitbucket_authorize_url: str | None = None
    bitbucket_token_url: str | None = None
    bitbucket_redirect_uri: str | None = None
    bitbucket_oauth_scope: str | None = None

    # Bitbucket
    bitbucket_host: str | None = None

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
            or (m.bitbucket_client_id and m.bitbucket_client_secret)
        ):
            raise ValueError(
                "You have to configure an api key, authorized groups or OAuth credentials"
            )

        return m

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

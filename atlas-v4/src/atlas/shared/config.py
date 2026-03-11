"""Atlas configuration using pydantic-settings.

Loads from environment variables with ATLAS_ prefix.
See PROJECT_CONVENTIONS.md Section 8.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class AtlasConfig(BaseSettings):
    """Central configuration for Atlas v4.

    All settings are loaded from environment variables with the ATLAS_ prefix.
    Example: ATLAS_PORT=8000 sets port=8000.
    """

    # Server
    port: int = 8000
    host: str = "127.0.0.1"
    log_level: str = "INFO"

    # LLM Providers
    default_llm_provider: str = "stub"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Feature Flags
    enable_voice: bool = False
    enable_learning: bool = True
    enable_self_modify: bool = False

    model_config = {"env_prefix": "ATLAS_"}


@lru_cache(maxsize=1)
def get_config() -> AtlasConfig:
    """Get the singleton Atlas configuration.

    Returns:
        The global AtlasConfig instance, loaded from environment.
    """
    return AtlasConfig()

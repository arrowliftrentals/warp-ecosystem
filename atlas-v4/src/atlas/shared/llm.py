"""LLM provider abstraction for model independence (R6).

Defines LLMProvider Protocol and concrete implementations.
Config selects provider via ATLAS_DEFAULT_LLM_PROVIDER.
"""

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from atlas.shared.config import get_config
from atlas.shared.errors import ConfigurationError, LLMProviderError


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM providers. All providers must implement this."""

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        """Generate a text completion.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt for context.

        Returns:
            The generated text response.

        Raises:
            LLMProviderError: If the API call fails.
        """
        ...

    async def complete_structured(
        self, prompt: str, schema: type[BaseModel], system_prompt: str = ""
    ) -> BaseModel:
        """Generate a structured completion matching a Pydantic schema.

        Args:
            prompt: The user prompt.
            schema: The Pydantic model to parse the response into.
            system_prompt: Optional system prompt for context.

        Returns:
            A Pydantic model instance parsed from the response.

        Raises:
            LLMProviderError: If the API call or parsing fails.
        """
        ...


class StubProvider:
    """Returns canned responses for testing without API keys.

    Satisfies R6: Atlas works without any specific LLM.
    """

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        """Return a canned response.

        Args:
            prompt: The user prompt (used to vary response).
            system_prompt: Ignored by stub.

        Returns:
            A deterministic stub response.
        """
        return (
            f"[StubProvider] I received your message: '{prompt[:50]}'. "
            "This is a stub response — configure a real LLM provider "
            "for production use."
        )

    async def complete_structured(
        self, prompt: str, schema: type[BaseModel], system_prompt: str = ""
    ) -> BaseModel:
        """Return a default instance of the requested schema.

        Args:
            prompt: The user prompt (ignored).
            schema: The Pydantic model to return a default instance of.
            system_prompt: Ignored by stub.

        Returns:
            A default-constructed instance of the schema.

        Raises:
            LLMProviderError: If default construction fails.
        """
        try:
            return schema.model_construct()
        except Exception as e:
            raise LLMProviderError(
                f"StubProvider failed to construct {schema.__name__}: {e}"
            ) from e


def get_llm_provider() -> LLMProvider:
    """Get the configured LLM provider.

    Returns:
        An LLMProvider instance based on ATLAS_DEFAULT_LLM_PROVIDER config.

    Raises:
        ConfigurationError: If the configured provider is unknown.
    """
    config = get_config()
    provider_name = config.default_llm_provider

    if provider_name == "stub":
        return StubProvider()
    elif provider_name == "openai":
        raise ConfigurationError(
            "OpenAI provider not yet implemented. Use 'stub' for now."
        )
    elif provider_name == "anthropic":
        raise ConfigurationError(
            "Anthropic provider not yet implemented. Use 'stub' for now."
        )
    else:
        raise ConfigurationError(
            f"Unknown LLM provider: {provider_name}. "
            "Valid options: openai, anthropic, stub"
        )

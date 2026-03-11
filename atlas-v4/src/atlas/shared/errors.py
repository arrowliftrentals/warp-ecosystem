"""Atlas error hierarchy.

All Atlas errors inherit from AtlasError. Never raise bare Exception.
See PROJECT_CONVENTIONS.md Section 6.
"""


class AtlasError(Exception):
    """Base for all Atlas errors. Never raise bare Exception."""


class ValidationError(AtlasError):
    """Data failed Pydantic or business rule validation."""


class MemoryLayerError(AtlasError):
    """Memory layer operation failed (read, write, query)."""


class GovernanceViolationError(AtlasError):
    """Action or output violated a governance rule. Blocks execution."""


class IntentParsingError(AtlasError):
    """Intent could not be determined from user input."""


class LLMProviderError(AtlasError):
    """LLM API call failed. System must degrade gracefully per R6."""


class ToolExecutionError(AtlasError):
    """Tool invocation failed."""


class SandboxError(AtlasError):
    """Sandbox execution failed."""


class ConfigurationError(AtlasError):
    """Invalid or missing configuration."""

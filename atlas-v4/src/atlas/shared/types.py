"""Shared type aliases and protocols for Atlas.

These types are used across subsystem boundaries.
"""

from typing import Literal, NewType

# Memory layer identifiers
LayerId = NewType("LayerId", str)
"""Memory layer identifier, e.g. 'l1', 'l2', ..., 'l10'."""

# Confidence scores (0.0 to 1.0)
ConfidenceScore = NewType("ConfidenceScore", float)
"""A confidence value between 0.0 and 1.0."""

# Session identifiers
SessionId = NewType("SessionId", str)
"""A unique conversation session identifier."""

# Intent classification
IntentLabel = NewType("IntentLabel", str)
"""An intent classification label, e.g. 'greeting', 'memory_store', 'search'."""

# LLM provider selection
LLMProviderName = Literal["openai", "anthropic", "stub"]
"""Valid LLM provider names."""

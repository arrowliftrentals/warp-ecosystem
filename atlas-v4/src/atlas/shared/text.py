"""Shared text utilities for Atlas.

System-wide text processing functions that apply across subsystem boundaries.
Promoted from Vol 9 governance (scrub_speculation) and Vol 5 intelligence
(detect_contradiction) to shared utility per C-24 and Vol 9 B.11 Discovery 11.1.

Owner: Vol 8 (API Infrastructure) per C-24 — shared utilities live in the
API layer's shared package. Consumed by Vol 2, Vol 5, Vol 9.

Architecture context:
    scrub_speculation: Deterministic regex replacements removing hedging language
        ("likely", "probably", "seems to be") from LLM-generated text. Originally
        in Vol 9 AnswerGovernor; promoted because ALL LLM text (commit messages,
        proposals, error explanations, learning summaries) benefits from scrubbing.

    detect_contradiction: Symbolic contradiction detection between two text spans.
        Used by Vol 5 intelligence pipeline and Vol 9 governance to flag internally
        inconsistent LLM outputs before they reach the user.
"""

from __future__ import annotations

import re

# --- Speculation Scrubbing (from Vol 9) ---

# Ordered by specificity: longer/more-specific patterns first.
# Per Vol 9 B.10 Lesson 10.2: reordering these patterns can produce garbled output.
# Regression tests MUST cover pattern ordering.
_SPECULATION_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    # Multi-word hedging phrases (most specific first)
    (re.compile(r"\bmost likely due to\b", re.IGNORECASE), "due to"),
    (re.compile(r"\bit is likely that\b", re.IGNORECASE), ""),
    (re.compile(r"\bit seems like\b", re.IGNORECASE), ""),
    (re.compile(r"\bit appears that\b", re.IGNORECASE), ""),
    (re.compile(r"\bseems to be\b", re.IGNORECASE), "is"),
    (re.compile(r"\bappears to be\b", re.IGNORECASE), "is"),
    (re.compile(r"\bmay be\b", re.IGNORECASE), "is"),
    (re.compile(r"\bmight be\b", re.IGNORECASE), "is"),
    # Single-word hedges (least specific last)
    (re.compile(r"\bprobably\b", re.IGNORECASE), ""),
    (re.compile(r"\blikely\b", re.IGNORECASE), ""),
    (re.compile(r"\bperhaps\b", re.IGNORECASE), ""),
    (re.compile(r"\bpossibly\b", re.IGNORECASE), ""),
]


def scrub_speculation(text: str) -> str:
    """Remove speculative/hedging language from text.

    Applies deterministic regex replacements to remove hedging words and phrases.
    Pattern order matters — see _SPECULATION_REPLACEMENTS docstring.

    Args:
        text: Input text potentially containing speculative language.

    Returns:
        Text with speculative language removed or replaced with assertive equivalents.
        Whitespace is normalized (no double spaces from removals).
    """
    result = text
    for pattern, replacement in _SPECULATION_REPLACEMENTS:
        result = pattern.sub(replacement, result)
    # Normalize whitespace from empty replacements
    result = re.sub(r"  +", " ", result).strip()
    return result


# --- Contradiction Detection (from Vol 5) ---


def detect_contradiction(span_a: str, span_b: str) -> bool:
    """Detect if two text spans contain contradictory claims.

    Symbolic contradiction detection using negation patterns and
    antonym matching. Used by Vol 5 intelligence and Vol 9 governance
    to flag internally inconsistent LLM outputs.

    Args:
        span_a: First text span.
        span_b: Second text span.

    Returns:
        True if a contradiction is detected between the spans.

    Note:
        Tier 0 implementation uses simple negation heuristics.
        Tier 2+ will add semantic similarity with threshold-based detection.
    """
    # Stub: Tier 0 implementation placeholder.
    # Real implementation will use:
    # 1. Negation detection (span_a affirms X, span_b negates X)
    # 2. Numeric contradiction (span_a says "5 files", span_b says "3 files")
    # 3. Antonym pairs ("increased" vs "decreased", "present" vs "absent")
    raise NotImplementedError(
        "detect_contradiction requires Tier 1+ implementation. "
        "See Vol 5 B.11 and Vol 9 B.11 for design requirements."
    )

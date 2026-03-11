"""Governance Pydantic schemas — the authoritative definitions.

Ownership: Volume 9 (Governance). Per C-01 and C-20 resolution, all
governance schemas live here, not in memory/schemas.py. No other
volume redefines these schemas.

Consumers: Vol 2 (Orchestrator), Vol 6 (Voice), Vol 7 (Console),
Vol 8 (API Infrastructure), Vol 10 (External Tools).

See: design-bible/09-governance.md B.6, design-bible/gate-output/
conflict-report.md C-01, C-20.
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from datetime import datetime

# ---------- Enums ----------

class AuthorityLevel(str, enum.Enum):
    """How well-grounded an output is in evidence."""

    GROUNDED = "GROUNDED"  # All claims verified against EvidenceStore
    ADVISORY = "ADVISORY"  # Partial evidence; hedging applied
    SPECULATIVE = "SPECULATIVE"  # No evidence; speculation scrubbed


class ClaimType(str, enum.Enum):
    """Classification of an extracted claim."""

    FACTUAL = "FACTUAL"
    PROCEDURAL = "PROCEDURAL"
    OPINION = "OPINION"
    META = "META"


class ClaimStatus(str, enum.Enum):
    """Verification status of an extracted claim."""

    GROUNDED = "GROUNDED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"
    HEDGED = "HEDGED"


class OutputPhase(str, enum.Enum):
    """Which phase of output governance produced this result."""

    EXTRACTION = "EXTRACTION"
    VERIFICATION = "VERIFICATION"
    SCORING = "SCORING"
    SCRUBBING = "SCRUBBING"
    FINAL = "FINAL"


class Approval(str, enum.Enum):
    """Final governance decision on output."""

    APPROVED = "approved"
    REVISE = "revise"
    BLOCKED = "blocked"


# ---------- Evidence schemas ----------

class EvidenceItem(BaseModel, frozen=True):
    """Verbatim record of a tool result stored in EvidenceStore."""

    id: str = Field(..., description="UUID4 evidence item ID")
    correlation_id: str = Field(..., description="Request correlation ID")
    tool_name: str
    args_hash: str = Field(..., description="SHA256 of serialized tool args")
    result_blob: Any = Field(..., description="Raw tool result (preserved verbatim)")
    result_sha256: str = Field(..., description="SHA256 of result for integrity")
    timestamp: datetime
    span_index: int = Field(default=0, description="Position in evidence chain")


class EvidenceContract(BaseModel, frozen=True):
    """Defines what evidence a claim type requires."""

    claim_type: ClaimType
    required_tools: list[str] = Field(default_factory=list)
    min_evidence_count: int = Field(default=1, ge=1)
    staleness_seconds: float = Field(default=300.0, gt=0)


# ---------- Claim schemas ----------

class ExtractedClaim(BaseModel, frozen=True):
    """A factual claim extracted from LLM output."""

    text: str = Field(..., min_length=1)
    claim_type: ClaimType
    source_span: tuple[int, int] = Field(..., description="(start, end) char offsets in original text")
    status: ClaimStatus = ClaimStatus.UNVERIFIED
    grounding_refs: list[str] = Field(default_factory=list, description="EvidenceItem IDs")
    verification_method: str = Field(default="none", description="How this claim was verified")


# ---------- Output governance schema ----------

class GovernedOutput(BaseModel, frozen=True):
    """Single egress schema for all user-facing text. Every LLM response
    passes through AnswerGovernor and is wrapped in this schema before
    reaching the user.

    This is the most important schema in the governance subsystem.
    """

    phase: OutputPhase
    authority_level: AuthorityLevel
    content: str = Field(..., description="The governed output text")
    content_sha256: str = Field(..., description="SHA256 of content for tamper detection")
    claims: list[ExtractedClaim] = Field(default_factory=list)
    grounding_refs: list[str] = Field(default_factory=list, description="EvidenceItem IDs referenced")
    approval: Approval
    policy_violations: list[str] = Field(default_factory=list)
    governor_latency_ms: float = Field(default=0.0, ge=0)


# ---------- Decision validation schemas ----------

class ValidationDecision(BaseModel, frozen=True):
    """Result of DecisionValidator.validate() — whether an intent is safe to execute."""

    intent: str
    allowed: bool
    reason: str = Field(default="")
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    policy_refs: list[str] = Field(default_factory=list, description="Policy IDs that informed decision")


class ContractResult(BaseModel, frozen=True):
    """Result of EvidenceContractRegistry.check() — whether evidence meets contract requirements."""

    claim_type: ClaimType
    satisfied: bool
    missing_tools: list[str] = Field(default_factory=list)
    evidence_count: int = Field(default=0, ge=0)
    staleness_ok: bool = Field(default=True)

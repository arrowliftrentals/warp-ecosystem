"""Structured logging configuration using structlog.

Every log entry is a JSON object with context.
See PROJECT_CONVENTIONS.md Section 7.
"""

import logging

import structlog


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structlog for Atlas.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR).
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a named logger.

    Args:
        name: The logger name, typically the module path.

    Returns:
        A bound structlog logger with the given name.
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]

import logging
import sys
import uuid
from contextvars import ContextVar

import structlog

correlation_id_ctx_var: ContextVar[str] = ContextVar("correlation_id", default="-")


def set_correlation_id(correlation_id: str | None = None) -> str:
    value = correlation_id or str(uuid.uuid4())
    correlation_id_ctx_var.set(value)
    return value


def get_correlation_id() -> str:
    return correlation_id_ctx_var.get()


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

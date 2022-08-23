"""logger lib"""

import logging

import structlog


def setup_logger(level=logging.INFO, style: str = "keys"):
    """setup logging"""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer()
    )
    if style == "json":
        formatter.processor = structlog.processors.JSONRenderer()
    else:
        formatter.processor = structlog.processors.KeyValueRenderer()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

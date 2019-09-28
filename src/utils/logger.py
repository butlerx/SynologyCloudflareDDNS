"""logger lib"""

from logging import INFO, StreamHandler, getLogger

from structlog import configure, dev, processors, stdlib


def setup_logger(level=INFO, style: str = "keys"):
    """setup logging"""
    configure(
        processors=[stdlib.add_log_level, stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=stdlib.LoggerFactory(),
    )

    formatter = stdlib.ProcessorFormatter(processor=dev.ConsoleRenderer())
    formatter.processor = processors.KeyValueRenderer()
    if style == "json":
        formatter.processor = processors.JSONRenderer()
    else:
        formatter.processor = processors.KeyValueRenderer()

    handler = StreamHandler()
    handler.setFormatter(formatter)
    root_logger = getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

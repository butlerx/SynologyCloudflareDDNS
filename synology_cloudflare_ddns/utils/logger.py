"""Logging setup with key=value and JSON output formats."""

from __future__ import annotations

import logging

from pythonjsonlogger import orjson

RESERVED_LOG_FIELDS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "asctime",
}


class KeyValueLogFormatter(logging.Formatter):
    """
    Format logs as a timestamp prefix followed by key=value pairs.

    Example: [2025-11-23T12:27:00] INFO     myapp                            User logged in user_id=42
    """

    def __init__(self, datefmt: str | None = "%Y-%m-%dT%H:%M:%S") -> None:
        """Create a formatter that renders timestamps with datefmt."""
        format_string = "[%(asctime)s] %(levelname)-8s %(name)-40s %(message)s"
        super().__init__(fmt=format_string, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """Render the record followed by its extra fields as key=value pairs."""
        if kv_pairs := [
            f"{key}={self._format_value(value)}"
            for key, value in record.__dict__.items()
            if key not in RESERVED_LOG_FIELDS and value is not None
        ]:
            record.msg = f"{record.msg} {' '.join(kv_pairs)}"

        result = super().format(record)

        # Add exception info if present
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if result[-1:] != "\n":
                result = result + "\n"
            result = result + record.exc_text

        return result

    def _format_value(self, value: object) -> str:
        value_str = str(value)
        if " " in value_str or "=" in value_str or '"' in value_str:
            clean_str = value_str.replace('"', '"')
            return f'"{clean_str}"'
        return value_str


class FieldLogger:
    """Wrap a logger so that key=value fields can be passed as keyword arguments."""

    def __init__(self, logger: logging.Logger) -> None:
        """Wrap logger."""
        self._logger = logger

    def debug(self, msg: str, *args: object, **fields: object) -> None:
        """Log a debug message with fields."""
        self._logger.debug(msg, *args, extra=fields)

    def info(self, msg: str, *args: object, **fields: object) -> None:
        """Log an info message with fields."""
        self._logger.info(msg, *args, extra=fields)

    def warning(self, msg: str, *args: object, **fields: object) -> None:
        """Log a warning message with fields."""
        self._logger.warning(msg, *args, extra=fields)

    def error(self, msg: str, *args: object, **fields: object) -> None:
        """Log an error message with fields."""
        self._logger.error(msg, *args, extra=fields)


def setup_logger(level: int = logging.INFO, log_format: str = "kv") -> None:
    """Send root logger output to stderr in the given format, kv or json."""
    handler = logging.StreamHandler()
    if log_format == "json":
        handler.setFormatter(orjson.OrjsonFormatter())
    else:
        handler.setFormatter(KeyValueLogFormatter())
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def get_logger(name: str | None = None) -> FieldLogger:
    """Return a logger with the given name that accepts key=value fields."""
    return FieldLogger(logging.getLogger(name))

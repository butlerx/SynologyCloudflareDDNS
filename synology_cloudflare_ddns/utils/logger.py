"""Logging setup with key=value and JSON output formats."""

from __future__ import annotations

import logging

from pythonjsonlogger import orjson

# Every attribute a bare LogRecord carries, so only fields passed via `extra=` are printed.
RESERVED_LOG_FIELDS = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message",
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
            clean_str = value_str.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{clean_str}"'
        return value_str


def setup_logger(level: int = logging.INFO, log_format: str = "kv") -> None:
    """Send root logger output to stderr in the given format, kv or json."""
    handler = logging.StreamHandler()
    if log_format == "json":
        handler.setFormatter(orjson.OrjsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    else:
        handler.setFormatter(KeyValueLogFormatter())
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def get_logger(name: str | None = None) -> logging.Logger:
    """Return the logger with the given name."""
    return logging.getLogger(name)

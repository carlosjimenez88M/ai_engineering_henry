"""Logging configuration with colored output for better readability.

This module provides a colored formatter for console logging that makes
it easier to scan logs during development and debugging. Colors are applied
based on log level (DEBUG=cyan, INFO=green, WARNING=yellow, ERROR=red, etc.).
"""

from __future__ import annotations

import logging


RESET = "\033[0m"
LEVEL_COLORS = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[35m",
}


class ColorFormatter(logging.Formatter):
    """Custom formatter that adds ANSI color codes based on log level.

    Colors are defined in LEVEL_COLORS dictionary. Extends the standard
    logging.Formatter to apply colors before returning formatted output.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Formats log record with appropriate color.

        Args:
            record: LogRecord to format.

        Returns:
            Formatted string with ANSI color codes.
        """
        color = LEVEL_COLORS.get(record.levelno, "")
        plain = super().format(record)
        return f"{color}{plain}{RESET}"


def get_logger(name: str = "brief_builder") -> logging.Logger:
    """Creates or retrieves a logger with colored console output.

    Configures a logger with:
    - INFO level by default
    - ColorFormatter for readable console output
    - StreamHandler writing to stderr
    - Format: timestamp | level | name | message

    The logger is configured once and reused on subsequent calls.

    Args:
        name: Logger name (default: "brief_builder").

    Returns:
        Configured Logger instance.

    Examples:
        >>> logger = get_logger()
        >>> logger.info("Starting brief generation")
        # Outputs colored log to console
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.propagate = False
    return logger

"""
Logging utilities for MCP File Server.

Provides structured logging with context and proper formatting.
"""

import logging
import sys


class ServerLogger:
    """
    Centralized logging for the MCP File Server.

    Provides structured logging with:
    - Standardized format
    - Context information
    - stderr output for MCP compatibility
    """

    def __init__(self, name: str = "mcp-file-server", level: str = "INFO"):
        """
        Initialize logger.

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Configure handler if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setLevel(getattr(logging, level.upper()))

            # Format: timestamp [LEVEL] message
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

    def debug(self, message: str, **kwargs):
        """Log debug message with optional context."""
        self.logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs):
        """Log info message with optional context."""
        self.logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs):
        """Log warning message with optional context."""
        self.logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs):
        """Log error message with optional context."""
        self.logger.error(self._format_message(message, **kwargs))

    def critical(self, message: str, **kwargs):
        """Log critical message with optional context."""
        self.logger.critical(self._format_message(message, **kwargs))

    def tool_called(self, tool_name: str, arguments: dict):
        """Log tool invocation."""
        self.info(f"Tool called: {tool_name}", arguments=arguments)

    def tool_success(self, tool_name: str, result_size: int | None = None):
        """Log successful tool execution."""
        msg = f"Tool succeeded: {tool_name}"
        if result_size:
            msg += f" (result size: {result_size} chars)"
        self.info(msg)

    def tool_error(self, tool_name: str, error: Exception):
        """Log tool execution error."""
        self.error(
            f"Tool failed: {tool_name}", error_type=type(error).__name__, error_message=str(error)
        )

    def _format_message(self, message: str, **kwargs) -> str:
        """
        Format message with optional context.

        Args:
            message: Main message
            **kwargs: Additional context to include

        Returns:
            Formatted message string
        """
        if not kwargs:
            return message

        context = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        return f"{message} [{context}]"


# Global logger instance
_logger: ServerLogger | None = None


def get_logger(name: str = "mcp-file-server", level: str = "INFO") -> ServerLogger:
    """
    Get or create the global logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        ServerLogger instance
    """
    global _logger
    if _logger is None:
        _logger = ServerLogger(name, level)
    return _logger


def set_log_level(level: str):
    """
    Set the logging level.

    Args:
        level: New logging level
    """
    logger = get_logger()
    logger.logger.setLevel(getattr(logging, level.upper()))
    for handler in logger.logger.handlers:
        handler.setLevel(getattr(logging, level.upper()))

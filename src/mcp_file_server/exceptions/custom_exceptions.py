"""
Custom exceptions for MCP File Server.

Following SOLID principles, we define specific exceptions for different error scenarios.
This makes error handling more precise and maintainable.
"""


class MCPFileServerError(Exception):
    """Base exception for all MCP File Server errors."""

    pass


class SecurityError(MCPFileServerError):
    """Raised when a security violation is detected (e.g., path traversal)."""

    pass


class FileAccessError(MCPFileServerError):
    """Raised when file access fails (permissions, not found, etc.)."""

    pass


class FileTypeNotSupportedError(MCPFileServerError):
    """Raised when attempting to process an unsupported file type."""

    pass


class FileSizeExceededError(MCPFileServerError):
    """Raised when file size exceeds configured limits."""

    pass


class InvalidArgumentError(MCPFileServerError):
    """Raised when tool receives invalid arguments."""

    pass


class ToolExecutionError(MCPFileServerError):
    """Raised when tool execution fails."""

    pass


class HandlerNotFoundError(MCPFileServerError):
    """Raised when no suitable handler is found for a file type."""

    pass

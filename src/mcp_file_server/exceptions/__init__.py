"""Exceptions package for MCP File Server."""

from .custom_exceptions import (
    FileAccessError,
    FileSizeExceededError,
    FileTypeNotSupportedError,
    HandlerNotFoundError,
    InvalidArgumentError,
    MCPFileServerError,
    SecurityError,
    ToolExecutionError,
)

__all__ = [
    "FileAccessError",
    "FileSizeExceededError",
    "FileTypeNotSupportedError",
    "HandlerNotFoundError",
    "InvalidArgumentError",
    "MCPFileServerError",
    "SecurityError",
    "ToolExecutionError",
]

"""Exceptions package for MCP File Server."""

from .custom_exceptions import (
    MCPFileServerError,
    SecurityError,
    FileAccessError,
    FileTypeNotSupportedError,
    FileSizeExceededError,
    InvalidArgumentError,
    ToolExecutionError,
    HandlerNotFoundError,
)

__all__ = [
    'MCPFileServerError',
    'SecurityError',
    'FileAccessError',
    'FileTypeNotSupportedError',
    'FileSizeExceededError',
    'InvalidArgumentError',
    'ToolExecutionError',
    'HandlerNotFoundError',
]

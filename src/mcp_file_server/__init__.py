"""
MCP File Server - Professional Implementation

A production-ready MCP server for file system operations.
"""

__version__ = "1.0.0"
__author__ = "MCP Learning Journey"

from .config import Config
from .server import MCPFileServer

__all__ = ["Config", "MCPFileServer", "__version__"]

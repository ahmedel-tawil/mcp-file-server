"""
Configuration management for MCP File Server.
"""

from pathlib import Path
from typing import Optional
import os

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """
    Central configuration class for the MCP File Server.
    
    Attributes:
        base_dir (Path): Base directory for file operations (security boundary)
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        max_file_size (int): Maximum file size in bytes
        allowed_extensions (set): Set of allowed file extensions
        enable_pdf_support (bool): Whether PDF support is enabled
    """

    def __init__(
            self,
            base_dir: Optional[Path] = None,
            log_level: str = "INFO",
            max_file_size: int = 10 * 1024 * 1024,  # 10MB default
    ):
        """
        Initialize configuration.
        
        Args:
            base_dir: Base directory for operations (defaults to ~/Documents)
            log_level: Logging level
            max_file_size: Maximum file size in bytes
        """
        self.base_dir = base_dir or Path.home() / "Documents"
        self.log_level = log_level
        self.max_file_size = max_file_size

        # File type support
        self.allowed_extensions = {
            '.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml',
            '.csv', '.html', '.css', '.xml', '.log', '.sh', '.pdf'
        }

        self.enable_pdf_support = True

        # Validate configuration
        self._validate()

    def _validate(self):
        """Validate configuration settings."""
        if not self.base_dir.exists():
            raise ValueError(f"Base directory does not exist: {self.base_dir}")

        if not self.base_dir.is_dir():
            raise ValueError(f"Base directory is not a directory: {self.base_dir}")

        if self.max_file_size <= 0:
            raise ValueError("max_file_size must be positive")

        valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.log_level}")

    def is_extension_allowed(self, extension: str) -> bool:
        """
        Check if a file extension is allowed.
        
        Args:
            extension: File extension (including the dot)
        
        Returns:
            True if extension is allowed
        """
        return extension.lower() in self.allowed_extensions

    @classmethod
    def from_env(cls) -> 'Config':
        """
        Create configuration from environment variables.
        
        Environment variables:
            MCP_BASE_DIR: Base directory path
            MCP_LOG_LEVEL: Logging level
            MCP_MAX_FILE_SIZE: Maximum file size in bytes
        
        Returns:
            Config instance
        """
        base_dir = os.getenv('MCP_BASE_DIR')
        if base_dir:
            base_dir = Path(base_dir)

        log_level = os.getenv('MCP_LOG_LEVEL', 'INFO')

        max_file_size = os.getenv('MCP_MAX_FILE_SIZE')
        if max_file_size:
            max_file_size = int(max_file_size)
        else:
            max_file_size = 10 * 1024 * 1024

        return cls(
            base_dir=base_dir,
            log_level=log_level,
            max_file_size=max_file_size
        )

    def __repr__(self) -> str:
        return (
            f"Config(base_dir={self.base_dir}, "
            f"log_level={self.log_level}, "
            f"max_file_size={self.max_file_size})"
        )

"""
Path validation utilities for security.

This module ensures all file operations stay within the allowed base directory,
preventing path traversal attacks and unauthorized file access.

"""

from pathlib import Path
from exceptions import SecurityError


class PathValidator:
    """
    Validates file paths for security compliance.
    
    Ensures paths:
    - Stay within the base directory (no path traversal)
    - Don't contain dangerous patterns
    - Are properly normalized
    """
    
    def __init__(self, base_dir: Path):
        """
        Initialize path validator.
        
        Args:
            base_dir: Base directory that all paths must be relative to
        """
        self.base_dir = base_dir.resolve()
    
    def validate(self, path: Path) -> Path:
        """
        Validate a path for security compliance.
        
        Args:
            path: Path to validate (can be relative or absolute)
        
        Returns:
            Resolved absolute path
        
        Raises:
            SecurityError: If path is outside base directory or contains dangerous patterns
        """
        # Convert to absolute path
        if not path.is_absolute():
            path = self.base_dir / path
        
        # Resolve to remove .. and symlinks
        try:
            resolved = path.resolve()
        except (OSError, RuntimeError) as e:
            raise SecurityError(f"Failed to resolve path: {e}")
        
        # Check if within base directory
        if not self._is_safe_path(resolved):
            raise SecurityError(
                f"Access denied: Path '{path}' is outside allowed directory '{self.base_dir}'"
            )
        
        return resolved
    
    def _is_safe_path(self, path: Path) -> bool:
        """
        Check if path is within the base directory.
        
        Args:
            path: Absolute, resolved path to check
        
        Returns:
            True if path is safe (within base directory)
        """
        try:
            # Check if path is relative to base_dir
            path.relative_to(self.base_dir)
            return True
        except ValueError:
            # Path is not relative to base_dir
            return False
    
    def validate_new_file(self, path: Path) -> Path:
        """
        Validate path for creating a new file.
        
        Similar to validate(), but doesn't require the file to exist.
        
        Args:
            path: Path for new file
        
        Returns:
            Validated path
        
        Raises:
            SecurityError: If path is unsafe
        """
        # For new files, validate the parent directory exists within bounds
        if not path.is_absolute():
            path = self.base_dir / path
        
        # Don't resolve yet (file doesn't exist), but check parent
        parent = path.parent
        
        try:
            resolved_parent = parent.resolve()
        except (OSError, RuntimeError) as e:
            raise SecurityError(f"Failed to resolve parent directory: {e}")
        
        if not self._is_safe_path(resolved_parent):
            raise SecurityError(
                f"Access denied: Path '{path}' is outside allowed directory"
            )
        
        # Return the non-resolved path (file doesn't exist yet)
        return path
    
    def get_relative_path(self, path: Path) -> Path:
        """
        Get path relative to base directory.
        
        Args:
            path: Absolute path to convert
        
        Returns:
            Path relative to base_dir
        
        Raises:
            ValueError: If path is not within base_dir
        """
        resolved = path.resolve()
        return resolved.relative_to(self.base_dir)

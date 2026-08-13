"""
File lister tool.

Lists files and directories in a given path.
Follows Single Responsibility Principle: Only lists directory contents.
"""

from typing import Any

from mcp.types import TextContent, Tool

from ..exceptions import FileAccessError
from .base_tool import BaseTool


class FileListerTool(BaseTool):
    """
    Tool for listing directory contents.

    Lists all files and subdirectories with visual indicators.
    """

    def get_definition(self) -> Tool:
        """Return the tool definition for MCP."""
        return Tool(
            name="list_files",
            description="List all files and directories in a given path",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path relative to Documents folder (empty string for root)",
                    }
                },
                "required": [],
            },
        )

    def _execute_impl(self, arguments: dict[str, Any]) -> list[TextContent]:
        """
        Execute directory listing.

        Args:
            arguments: Optional 'path' key (defaults to empty string for root)

        Returns:
            Formatted list of files and directories

        Raises:
            FileAccessError: If directory cannot be accessed
        """
        # Get path (default to root)
        rel_path = arguments.get("path", "")

        if rel_path:
            target_dir = self.config.base_dir / rel_path
        else:
            target_dir = self.config.base_dir

        # Validate path
        validated_path = self.validator.validate(target_dir)

        # Check it's a directory
        if not validated_path.is_dir():
            raise FileAccessError(f"Path is not a directory: {rel_path}")

        # List contents
        try:
            items = []
            for item in sorted(validated_path.iterdir()):
                # Skip hidden files (starting with .)
                if item.name.startswith("."):
                    continue

                # Add emoji indicator
                if item.is_dir():
                    emoji = "directory"
                    items.append(f"{emoji}: {item.name}")
                else:
                    emoji = "file"
                    # Add file size for files
                    size = item.stat().st_size
                    size_str = self._format_size(size)
                    items.append(f"{emoji}: {item.name} ({size_str})")

            # Return formatted list
            return self.formatter.file_list(
                items=items, empty_message=f"Directory is empty: {rel_path or 'root'}"
            )

        except PermissionError as e:
            raise FileAccessError(f"Permission denied: {e}")
        except Exception as e:
            raise FileAccessError(f"Failed to list directory: {e}")

    @staticmethod
    def _format_size(size: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

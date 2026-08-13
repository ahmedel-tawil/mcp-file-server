"""
File creator tool.

Creates new files only - fails if file already exists.
Follows Single Responsibility Principle: Only creates new files.
"""

from pathlib import Path
from typing import Any

from mcp.types import TextContent, Tool

from ..exceptions import FileAccessError
from ..handlers import TextHandler
from .base_tool import BaseTool


class FileCreatorTool(BaseTool):
    """
    Tool for creating new files safely.

    Fails if file already exists to prevent accidental overwrites.
    This is the safer alternative to file_writer.
    """

    def get_definition(self) -> Tool:
        """Return the tool definition for MCP."""
        return Tool(
            name="create_file",
            description="Create a new file with content. Will fail if file already exists.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to Documents folder",
                    },
                    "content": {"type": "string", "description": "Content to write to the file"},
                },
                "required": ["path", "content"],
            },
        )

    def _execute_impl(self, arguments: dict[str, Any]) -> list[TextContent]:
        """
        Execute file creation.

        Args:
            arguments: Must contain 'path' and 'content' keys

        Returns:
            Success message with file info

        Raises:
            FileAccessError: If file cannot be created or already exists
        """
        # Get arguments
        rel_path = arguments["path"]
        content = arguments["content"]

        file_path = Path(rel_path)

        # Validate path for new file
        validated_path = self.validator.validate_new_file(self.config.base_dir / file_path)

        # Check if file already exists
        if validated_path.exists():
            raise FileAccessError(
                f"File already exists at '{rel_path}'. Use write_file to overwrite."
            )

        # Create parent directories if needed
        validated_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the file
        try:
            size = TextHandler.write(validated_path, content)
        except PermissionError as e:
            raise FileAccessError(f"Permission denied: {e}")
        except Exception as e:
            raise FileAccessError(f"Failed to create file: {e}")

        # Return success response
        return self.formatter.file_created(file_path=str(rel_path), size=size)

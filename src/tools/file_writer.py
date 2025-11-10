"""
File writer tool.

Writes content to files, creating new or overwriting existing files.
Follows Single Responsibility Principle: Only writes files.
"""

from pathlib import Path
from typing import List, Dict, Any
from mcp.types import Tool, TextContent

from tools.base_tool import BaseTool
from handlers import TextHandler
from exceptions import FileAccessError


class FileWriterTool(BaseTool):
    """
    Tool for writing file contents.
    
    Creates new files or overwrites existing files.
    Always writes as text files.
    """
    
    def get_definition(self) -> Tool:
        """Return the tool definition for MCP."""
        return Tool(
            name="write_file",
            description="Write content to a file. Creates new file or overwrites existing file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to Documents folder"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["path", "content"]
            }
        )
    
    def _execute_impl(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Execute file writing.
        
        Args:
            arguments: Must contain 'path' and 'content' keys
        
        Returns:
            Success message with file info
        
        Raises:
            FileAccessError: If file cannot be written
        """
        # Get arguments
        rel_path = arguments["path"]
        content = arguments["content"]
        
        file_path = Path(rel_path)
        
        # Validate path for new file creation
        validated_path = self.validator.validate_new_file(
            self.config.base_dir / file_path
        )
        
        # Check if we're overwriting
        existed = validated_path.exists()
        
        # Create parent directories if needed
        validated_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        try:
            size = TextHandler.write(validated_path, content)
        except PermissionError as e:
            raise FileAccessError(f"Permission denied: {e}")
        except Exception as e:
            raise FileAccessError(f"Failed to write file: {e}")
        
        # Return success response
        return self.formatter.file_written(
            file_path=str(rel_path),
            size=size,
            overwritten=existed
        )

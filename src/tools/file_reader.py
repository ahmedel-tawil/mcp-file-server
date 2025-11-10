"""
File reader tool.

Reads content from text and PDF files.
Follows Single Responsibility Principle: Only reads files.
"""

from pathlib import Path
from typing import List, Dict, Any
from mcp.types import Tool, TextContent

from tools.base_tool import BaseTool
from handlers import TextHandler, PDFHandler
from exceptions import FileAccessError, FileTypeNotSupportedError


class FileReaderTool(BaseTool):
    """
    Tool for reading file contents.
    
    Supports:
    - Text files (.txt, .md, .py, .json, etc.)
    - PDF files (.pdf)
    
    Automatically selects the appropriate handler based on file extension.
    """
    
    def get_definition(self) -> Tool:
        """Return the tool definition for MCP."""
        return Tool(
            name="read_file",
            description="Read the contents of a text or PDF file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to Documents folder"
                    }
                },
                "required": ["path"]
            }
        )
    
    def _execute_impl(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Execute file reading.
        
        Args:
            arguments: Must contain 'path' key
        
        Returns:
            List containing file content
        
        Raises:
            FileAccessError: If file cannot be read
            FileTypeNotSupportedError: If file type is not supported
        """
        # Get and validate path
        rel_path = arguments["path"]
        file_path = Path(rel_path)
        
        # Validate security
        validated_path = self.validator.validate(
            self.config.base_dir / file_path
        )
        
        # Check file exists
        if not validated_path.exists():
            raise FileAccessError(f"File not found: {rel_path}")
        
        if not validated_path.is_file():
            raise FileAccessError(f"Path is not a file: {rel_path}")
        
        # Select appropriate handler
        content = self._read_with_handler(validated_path)
        
        # Return formatted response
        return self.formatter.file_content(
            content,
            file_path=str(rel_path)
        )
    
    def _read_with_handler(self, file_path: Path) -> str:
        """
        Read file using the appropriate handler.
        
        Args:
            file_path: Validated path to file
        
        Returns:
            File content as string
        
        Raises:
            FileTypeNotSupportedError: If no handler supports the file type
            FileAccessError: If reading fails
        """
        # Try PDF handler
        if PDFHandler.can_handle(file_path):
            try:
                return PDFHandler.read(file_path)
            except PermissionError as e:
                raise FileAccessError(f"Cannot read PDF: {e}")
            except Exception as e:
                raise FileAccessError(f"Failed to read PDF: {e}")
        
        # Try text handler
        if TextHandler.can_handle(file_path):
            try:
                return TextHandler.read(file_path)
            except UnicodeDecodeError:
                raise FileAccessError(
                    f"File appears to be binary: {file_path.name}. "
                    "Only text and PDF files are supported."
                )
            except Exception as e:
                raise FileAccessError(f"Failed to read file: {e}")
        
        # No handler found
        raise FileTypeNotSupportedError(
            f"Unsupported file type: {file_path.suffix}. "
            f"Supported types: {', '.join(TextHandler.SUPPORTED_EXTENSIONS | {'.pdf'})}"
        )

"""
Response formatting utilities.

Standardizes response format for all tools, ensuring consistency.
"""

from typing import List, Optional
from mcp.types import TextContent


class ResponseFormatter:
    """
    Formats tool responses in a consistent way.
    
    Provides helper methods for creating standardized responses:
    - Success messages
    - Error messages
    - File content responses
    - List responses
    """
    
    @staticmethod
    def success(message: str) -> List[TextContent]:
        """
        Create a success response.
        
        Args:
            message: Success message
        
        Returns:
            List of TextContent
        """
        return [TextContent(type="text", text=f"✅ {message}")]
    
    @staticmethod
    def error(message: str) -> List[TextContent]:
        """
        Create an error response.
        
        Args:
            message: Error message
        
        Returns:
            List of TextContent
        """
        return [TextContent(type="text", text=f"❌ Error: {message}")]
    
    @staticmethod
    def file_content(content: str, file_path: Optional[str] = None) -> List[TextContent]:
        """
        Create a file content response.
        
        Args:
            content: File content
            file_path: Optional file path to include in response
        
        Returns:
            List of TextContent
        """
        if file_path:
            header = f"📄 Content of '{file_path}':\n\n"
            return [TextContent(type="text", text=header + content)]
        return [TextContent(type="text", text=content)]
    
    @staticmethod
    def file_list(items: List[str], empty_message: str = "Directory is empty") -> List[TextContent]:
        """
        Create a file list response.
        
        Args:
            items: List of items (with emojis already included)
            empty_message: Message to show if list is empty
        
        Returns:
            List of TextContent
        """
        if not items:
            return [TextContent(type="text", text=empty_message)]
        
        content = "\n".join(items)
        return [TextContent(type="text", text=content)]
    
    @staticmethod
    def file_created(file_path: str, size: int) -> List[TextContent]:
        """
        Create a file creation success response.
        
        Args:
            file_path: Path of created file
            size: Size of content in characters
        
        Returns:
            List of TextContent
        """
        message = f"✅ Successfully created file: {file_path}\n📊 Size: {size} characters"
        return [TextContent(type="text", text=message)]
    
    @staticmethod
    def file_written(file_path: str, size: int, overwritten: bool = False) -> List[TextContent]:
        """
        Create a file write success response.
        
        Args:
            file_path: Path of written file
            size: Size of content in characters
            overwritten: Whether file was overwritten
        
        Returns:
            List of TextContent
        """
        action = "overwritten" if overwritten else "created"
        message = f"✅ Successfully {action} file: {file_path}\n📊 Size: {size} characters"
        return [TextContent(type="text", text=message)]
    
    @staticmethod
    def search_results(matches: List[str], pattern: str) -> List[TextContent]:
        """
        Create a search results response.
        
        Args:
            matches: List of matching file paths
            pattern: Search pattern used
        
        Returns:
            List of TextContent
        """
        if not matches:
            return [TextContent(type="text", text=f"No files found matching pattern: {pattern}")]
        
        header = f"🔍 Found {len(matches)} file(s) matching '{pattern}':\n\n"
        content = header + "\n".join(matches)
        return [TextContent(type="text", text=content)]
    
    @staticmethod
    def info(message: str, details: Optional[dict] = None) -> List[TextContent]:
        """
        Create an info response with optional details.
        
        Args:
            message: Main message
            details: Optional dictionary of details
        
        Returns:
            List of TextContent
        """
        text = f"ℹ️ {message}"
        
        if details:
            text += "\n\nDetails:\n"
            for key, value in details.items():
                text += f"  • {key}: {value}\n"
        
        return [TextContent(type="text", text=text)]

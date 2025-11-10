"""
File searcher tool.

Searches for files matching a pattern recursively.
Follows Single Responsibility Principle: Only searches files.
"""

from pathlib import Path
from typing import List, Dict, Any
from mcp.types import Tool, TextContent

from tools.base_tool import BaseTool
from exceptions import FileAccessError


class FileSearcherTool(BaseTool):
    """
    Tool for searching files by pattern.
    
    Performs recursive glob search from the base directory.
    """
    
    def get_definition(self) -> Tool:
        """Return the tool definition for MCP."""
        return Tool(
            name="search_files",
            description="Search for files by name pattern (e.g., '*.pdf', 'report*', '*.txt')",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern using wildcards (* and ?)"
                    }
                },
                "required": ["pattern"]
            }
        )
    
    def _execute_impl(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Execute file search.
        
        Args:
            arguments: Must contain 'pattern' key
        
        Returns:
            List of matching file paths
        
        Raises:
            FileAccessError: If search fails
        """
        # Get pattern
        pattern = arguments["pattern"]
        
        # Perform recursive search
        try:
            matches = []
            
            # Use rglob for recursive search
            for file_path in self.config.base_dir.rglob(pattern):
                # Skip directories, only return files
                if not file_path.is_file():
                    continue
                
                # Skip hidden files
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                
                # Get path relative to base_dir
                try:
                    rel_path = file_path.relative_to(self.config.base_dir)
                    matches.append(str(rel_path))
                except ValueError:
                    # Skip files outside base_dir (shouldn't happen, but safe)
                    continue
            
            # Return formatted results
            return self.formatter.search_results(
                matches=matches,
                pattern=pattern
            )
            
        except Exception as e:
            raise FileAccessError(f"Search failed: {e}")

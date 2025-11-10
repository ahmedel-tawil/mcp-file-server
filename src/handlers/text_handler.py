"""
Text file handler.

Handles reading and writing plain text files.
Single Responsibility: Text file I/O only.
"""

from pathlib import Path
from typing import Optional


class TextHandler:
    """
    Handler for plain text files.
    
    Supports common text file formats:
    - .txt, .md, .py, .js, .json, .yaml, .csv, .html, .css, .xml, .log, etc.
    """
    
    SUPPORTED_EXTENSIONS = {
        '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx',
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.csv', '.tsv', '.html', '.htm', '.css', '.scss',
        '.xml', '.log', '.sh', '.bash', '.zsh', '.fish',
        '.sql', '.r', '.cpp', '.c', '.h', '.java', '.kt',
        '.swift', '.go', '.rs', '.rb', '.php', '.pl', '.lua'
    }
    
    @classmethod
    def can_handle(cls, file_path: Path) -> bool:
        """
        Check if this handler can process the given file.
        
        Args:
            file_path: Path to check
        
        Returns:
            True if this handler supports the file type
        """
        return file_path.suffix.lower() in cls.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def read(file_path: Path, encoding: str = 'utf-8') -> str:
        """
        Read text file content.
        
        Args:
            file_path: Path to file
            encoding: Text encoding (default: utf-8)
        
        Returns:
            File content as string
        
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            UnicodeDecodeError: If file encoding is wrong
        """
        return file_path.read_text(encoding=encoding)
    
    @staticmethod
    def write(file_path: Path, content: str, encoding: str = 'utf-8') -> int:
        """
        Write content to text file.
        
        Args:
            file_path: Path to file
            content: Content to write
            encoding: Text encoding (default: utf-8)
        
        Returns:
            Number of characters written
        
        Raises:
            PermissionError: If file can't be written
        """
        file_path.write_text(content, encoding=encoding)
        return len(content)
    
    @staticmethod
    def get_info(file_path: Path) -> dict:
        """
        Get information about a text file.
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary with file information
        """
        stat = file_path.stat()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
        except Exception:
            lines = None
        
        return {
            'type': 'text',
            'extension': file_path.suffix,
            'size_bytes': stat.st_size,
            'lines': lines,
            'encoding': 'utf-8'
        }

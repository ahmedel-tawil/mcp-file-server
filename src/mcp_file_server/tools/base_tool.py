"""
Base tool class for all MCP tools.

This abstract base class defines the interface that all tools must implement,
following the Open/Closed Principle and Liskov Substitution Principle.
"""

from abc import ABC, abstractmethod
from typing import Any

from mcp.types import TextContent, Tool

from ..config import Config
from ..utils import PathValidator, ResponseFormatter, get_logger


class BaseTool(ABC):
    """
    Abstract base class for all MCP tools.

    This class provides:
    - Common infrastructure (config, validator, logger, formatter)
    - Template method pattern for execution
    - Standardized error handling

    Subclasses must implement:
    - get_definition(): Return tool definition
    - _execute_impl(): Actual tool logic
    """

    def __init__(self, config: Config):
        """
        Initialize base tool.

        Args:
            config: Server configuration
        """
        self.config = config
        self.validator = PathValidator(config.base_dir)
        self.logger = get_logger()
        self.formatter = ResponseFormatter()

    @abstractmethod
    def get_definition(self) -> Tool:
        """
        Get the tool definition for MCP.

        Returns:
            Tool definition with name, description, and input schema
        """
        pass

    @abstractmethod
    def _execute_impl(self, arguments: dict[str, Any]) -> list[TextContent]:
        """
        Execute the tool's core logic.

        Args:
            arguments: Tool arguments from MCP client

        Returns:
            List of TextContent responses

        Raises:
            Various exceptions based on the tool's requirements
        """
        pass

    def execute(self, arguments: dict[str, Any]) -> list[TextContent]:
        """
        Execute the tool with error handling and logging.

        This is a template method that:
        1. Logs the invocation
        2. Calls the implementation
        3. Handles errors
        4. Logs the result

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent responses
        """
        tool_name = self.get_definition().name

        try:
            # Log invocation
            self.logger.tool_called(tool_name, arguments)

            # Execute implementation
            result = self._execute_impl(arguments)

            # Log success
            result_size = sum(len(r.text) for r in result if hasattr(r, "text"))
            self.logger.tool_success(tool_name, result_size)

            return result

        except Exception as e:
            # Log error
            self.logger.tool_error(tool_name, e)

            # Return formatted error
            error_message = f"{type(e).__name__}: {e!s}"
            return self.formatter.error(error_message)

    def get_name(self) -> str:
        """Get the tool name."""
        return self.get_definition().name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.get_name()}')"

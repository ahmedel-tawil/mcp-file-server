"""
MCP File Server - Main Entry Point

Professional implementation of an MCP server for file system operations.
"""

import asyncio
import sys

import mcp.server.stdio
from mcp.server import Server
from mcp.types import TextContent

# Import our modules
from .config import Config
from .tools import (
    FileCreatorTool,
    FileListerTool,
    FileReaderTool,
    FileSearcherTool,
    FileWriterTool,
)
from .utils import get_logger


class MCPFileServer:
    """
    Main MCP File Server.

    Coordinates all tools and handles MCP protocol communication.
    """

    def __init__(self, config: Config):
        """
        Initialize the MCP File Server.

        Args:
            config: Server configuration
        """
        self.config = config
        self.logger = get_logger(level=config.log_level)
        self.app = Server("mcp-file-server-pro")

        # Initialize all tools
        self.tools = self._initialize_tools()

        # Register handlers
        self._register_handlers()

        self.logger.info(
            "MCP File Server initialized", base_dir=str(config.base_dir), tool_count=len(self.tools)
        )

    def _initialize_tools(self) -> list:
        """
        Initialize all available tools.

        Returns:
            List of tool instances
        """
        tools = [
            FileReaderTool(self.config),
            FileWriterTool(self.config),
            FileCreatorTool(self.config),
            FileListerTool(self.config),
            FileSearcherTool(self.config),
        ]

        self.logger.info(
            f"Initialized {len(tools)} tools", tools=[tool.get_name() for tool in tools]
        )

        return tools

    def _register_handlers(self):
        """Register MCP protocol handlers."""

        @self.app.list_tools()
        async def list_tools():
            """
            Handle tools/list request.

            Returns list of all available tools with their definitions.
            """
            self.logger.debug("Tools list requested")

            return [tool.get_definition() for tool in self.tools]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: dict):
            """
            Handle tools/call request.

            Routes the call to the appropriate tool.

            Args:
                name: Tool name to execute
                arguments: Tool arguments

            Returns:
                Tool execution result
            """
            self.logger.debug("Tool call requested", tool=name)

            # Find the tool
            tool = self._find_tool(name)

            if tool is None:
                error_msg = f"Unknown tool: {name}"
                self.logger.error(error_msg)
                return [TextContent(type="text", text=f"❌ Error: {error_msg}")]

            # Execute the tool
            # The tool's execute() method handles all error handling and logging
            result = tool.execute(arguments)

            return result

    def _find_tool(self, name: str):
        """
        Find a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        for tool in self.tools:
            if tool.get_name() == name:
                return tool
        return None

    async def run(self):
        """
        Run the MCP server.

        Sets up stdio transport and starts the server loop.
        """
        self.logger.info("Starting MCP File Server...")

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            self.logger.info("Server ready and listening")

            await self.app.run(read_stream, write_stream, self.app.create_initialization_options())


async def async_main():
    """
    Async entry point.

    Creates configuration, initializes server, and runs it.
    """
    # Configuration comes from the environment so the sandbox root is
    # explicit and deployable (MCP_BASE_DIR, MCP_LOG_LEVEL, MCP_MAX_FILE_SIZE).
    # Defaults to ~/Documents.
    config = Config.from_env()

    # Create and run server
    server = MCPFileServer(config)
    await server.run()


def main():
    """
    Console-script entry point (``mcp-file-server``).

    Synchronous wrapper so it can be referenced from [project.scripts].
    """
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n✋ Server stopped by user", file=sys.stderr)


if __name__ == "__main__":
    main()

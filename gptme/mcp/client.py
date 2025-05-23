import asyncio
import logging
from contextlib import AsyncExitStack
import os

from gptme.config import Config, get_config

import mcp.types as types  # Import all types
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

logger = logging.getLogger(__name__)


class MCPClient:
    """A client for interacting with MCP servers"""

    def __init__(self, config: Config | None = None):
        """Initialize the client with optional config"""
        self.config = config or get_config()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        logger.debug(f"Init - Loop ID: {id(self.loop)}")
        self.session: ClientSession | None = None
        self.tools: types.ListToolsResult | None = None
        self.stack: AsyncExitStack | None = None

    def _run_async(self, coro):
        """Run a coroutine in the event loop."""
        try:
            logger.debug(f"_run_async start - Loop ID: {id(self.loop)}")
            result = self.loop.run_until_complete(coro)
            logger.debug(f"_run_async end - Loop ID: {id(self.loop)}")
            return result
        except Exception as e:
            logger.debug(f"_run_async failed with error: {e}")
            raise

    async def _read_stderr(self, stderr):
        """Read stderr without blocking the main flow"""
        try:
            while True:
                line = await stderr.readline()
                if not line:
                    break
                logger.debug(f"Server stderr: {line.decode().strip()}")
        except Exception as e:
            logger.debug(f"Stderr reader stopped: {e}")

    async def _setup_connection(
        self, server_params
    ) -> tuple[types.ListToolsResult, ClientSession]:
        """Set up the connection and maintain it"""
        self.stack = AsyncExitStack()
        await self.stack.__aenter__()

        try:
            transport = await self.stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = transport

            csession = ClientSession(read, write)
            session = await self.stack.enter_async_context(csession)
            self.session = session  # Assign to self.session after the await

            if not self.session:
                raise RuntimeError("Failed to initialize session")

            await asyncio.wait_for(self.session.initialize(), timeout=5.0)
            tools = await asyncio.wait_for(self.session.list_tools(), timeout=10.0)
            self.tools = tools  # Assign after await

            if not self.tools:
                raise RuntimeError("Failed to get tools list")

            return (self.tools, self.session)
        except Exception:
            if self.stack:
                await self.stack.__aexit__(None, None, None)
                self.stack = None
            raise

    def connect(self, server_name: str) -> tuple[types.ListToolsResult, ClientSession]:
        """Connect to an MCP server by name"""
        if not self.config.mcp.enabled:
            raise RuntimeError("MCP is not enabled in config")

        server = next(
            (s for s in self.config.mcp.servers if s.name == server_name), None
        )
        if not server:
            raise ValueError(f"No MCP server config found for '{server_name}'")

        env = server.env or {}

        # Add env vars to the environment
        env.update(os.environ)

        params = StdioServerParameters(
            command=server.command, args=server.args, env=env
        )

        tools, session = self._run_async(self._setup_connection(params))
        logger.info(f"Tools: {tools}")
        return tools, session

    def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Synchronous tool call method"""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        async def _call_tool():
            session = self.session
            if session is None:
                raise RuntimeError("Should not be None")

            result = await session.call_tool(tool_name, arguments)
            # Safely access content for logging
            if (
                hasattr(result, "content")
                and result.content
                and len(result.content) > 0
                and isinstance(result.content[0], types.TextContent)
            ):
                content_text = result.content[0].text
                logger.debug(f"result {content_text}")

            if hasattr(result, "content") and result.content:
                for content in result.content:
                    if (
                        hasattr(content, "type")
                        and content.type == "text"
                        and hasattr(content, "text")
                    ):
                        return content.text
            return str(result)

        return self._run_async(_call_tool())

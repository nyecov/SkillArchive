import asyncio
import json
import logging
import sys
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_test_client")

async def run_verification():
    """
    Connects to the Context Engine Docker container via stdio and requests the available tools.
    """
    # The command needs to run the docker container interactively but without a TTY
    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",                           # Keep STDIN open even if not attached
            "--rm",                         # Remove container when done
            "-v", "g:/Skill Archive:/workspace", # Mount the workspace
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", "MEMORY_DIR=/workspace/temp__mem/Head/server/.gemini/mem",
            "context-engine-go:latest"
        ]
    )

    logger.info("Starting Context Engine MCP Server via Docker stdio...")
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            logger.info("Initializing MCP Session...")
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                logger.info("Requesting Tool List from Server...")
                # Request the tools available on the server
                response = await session.list_tools()
                
                logger.info("\n=== VERIFICATION RESULTS: AVAILABLE TOOLS ===")
                for tool in response.tools:
                    print(f"\n✅ Tool: {tool.name}")
                    print(f"   Description: {tool.description}")
                    
                    # Dump JSON schema beautifully
                    schema_json = json.dumps(tool.inputSchema, indent=2)
                    print(f"   Schema:\n{schema_json}")

                logger.info("\n=== DIAGNOSTICS LOG ===")
                print("Checking if boot diagnostics passed successfully.")
                print("If the tools listed above include log_session_finding and ingest_context, the Poka-yoke Boot Sequence succeeded without halting the server process.")
                
    except Exception as e:
        logger.error(f"Verification Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Windows specific fix for asyncio
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(run_verification())

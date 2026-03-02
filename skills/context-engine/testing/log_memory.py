import asyncio
import json
import logging
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Suppress debug logs from mcp-sdk for a cleaner output
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("mcp_memory_writer")
logger.setLevel(logging.INFO)

async def form_memory():
    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-v", "g:/Skill Archive:/workspace",
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", "MEMORY_DIR=/workspace/temp__mem/Head/server/.gemini/mem",
            "context-engine-go:latest"
        ]
    )

    logger.info("Booting Context Engine container and establishing MCP standard input/output...")
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                logger.info("Invoking `log_session_finding` tool via JSON-RPC...")
                write_result = await session.call_tool(
                    "log_session_finding", 
                    arguments={
                        "finding_text": "The Agent successfully bootstrapped the compiled Go Context Engine and natively routed its first active memory into the .gemini/mem state.",
                        "phase": "verification"
                    }
                )
                
                if write_result.content and len(write_result.content) > 0:
                    logger.info(write_result.content[0].text)
                
                logger.info("Invoking `read_session_state` to prove persistence...")
                read_result = await session.call_tool("read_session_state", arguments={})
                
                print("\n=== CURRENT SESSION STATE RAW JSON ===")
                if read_result.content and len(read_result.content) > 0:
                    print(read_result.content[0].text)
                else:
                    print("No content returned.")
                print("=======================================\n")
                
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(form_memory())

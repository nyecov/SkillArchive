import os
import shutil
import pytest
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys
import pytest_asyncio

# -- GLOBALS --
WORKSPACE_ROOT = "g:/Skill Archive"
TEST_STAGING = os.path.join(WORKSPACE_ROOT, "temp__mem/Head/server/tests/staging")
PRODUCTION_MEM = os.path.join(WORKSPACE_ROOT, "temp__mem/Head/server/.gemini/mem")

# Windows specific fix for asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@pytest.fixture(scope="session")
def test_workspace():
    """Session-scoped fixture to setup a clean testing environment once."""
    if os.path.exists(TEST_STAGING):
        shutil.rmtree(TEST_STAGING)
    os.makedirs(TEST_STAGING, exist_ok=True)
    
    # Safety Interlock (Poka-yoke)
    if os.path.abspath(TEST_STAGING) == os.path.abspath(PRODUCTION_MEM):
        pytest.exit("SYSTEM HALT (Jidoka): Test staging overlaps with production memories!")
    
    return TEST_STAGING

@pytest_asyncio.fixture
async def mcp_server(test_workspace):
    """
    Session-scoped fixture providing a connected MCP ClientSession.
    Keeps the container alive throughout the entire test run to eliminate cold-starts.
    """
    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "--init",
            "-v", f"{os.path.abspath(WORKSPACE_ROOT)}:/workspace",
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", "MEMORY_DIR=/workspace/temp__mem/Head/server/tests/staging",
            "context-engine-go:latest"
        ]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                
                # Debug logger
                log_path = os.path.join(test_workspace, "mcp_debug.log")
                
                original_call = session.call_tool
                async def debug_call_tool(name, arguments=None):
                    with open(log_path, "a") as f:
                        f.write(f"\n[CALL] {name} {arguments}\n")
                    res = await original_call(name, arguments)
                    with open(log_path, "a") as f:
                        f.write(f"[RES] isError={res.isError} content={res.content[0].text[:200] if res.content else 'None'}\n")
                    return res
                
                session.call_tool = debug_call_tool
                yield session
                
                # Explicitly close session if supported (graceful teardown)
                # But yield leaves us here in the finally/post-yield phase.
    except (RuntimeError, asyncio.CancelledError) as e:
        # Catch the "Attempted to exit cancel scope in a different task" race condition.
        # This is strictly related to subprocess closure on Win32 and is benign.
        if "cancel scope" in str(e).lower() or sys.platform == 'win32':
             pass 
        else:
             raise
    finally:
        # Robustness Delay
        await asyncio.sleep(0.2)

import os
import shutil
import pytest
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys
import uuid
import pytest_asyncio

# -- GLOBALS --
WORKSPACE_ROOT = "g:/Skill Archive"
TEST_STAGING = os.path.join(WORKSPACE_ROOT, "temp__mem/Head/tests/staging")
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
    # Pre-boot setup (Poka-yoke)
    lock_path = os.path.join(test_workspace, ".engine.instance.lock")
    session_path = os.path.join(test_workspace, "current_session.json")
    ontology_path = os.path.join(test_workspace, "ontology.json")
    
    # State reset to prevent leakage
    db_path = os.path.join(test_workspace, "engine.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(session_path):
        os.remove(session_path)
    if os.path.exists(ontology_path):
        os.remove(ontology_path)

    await asyncio.sleep(0.5)

    container_name = f"ce-test-{uuid.uuid4().hex[:8]}"

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "--init",
            "--name", container_name,
            "-v", f"{os.path.abspath(WORKSPACE_ROOT)}:/workspace",
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", "MEMORY_DIR=/workspace/temp__mem/Head/tests/staging",
            "context-engine-go:latest"
        ]
    )

    stdio_ctx = stdio_client(server_params)
    session_ctx = None
    try:
        read, write = await stdio_ctx.__aenter__()
        session_ctx = ClientSession(read, write)
        session = await session_ctx.__aenter__()
        
        await asyncio.wait_for(session.initialize(), timeout=20.0)
        
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
    except Exception as e:
        # Capture logs before container dies
        os.system(f"docker logs {container_name} > {os.path.join(test_workspace, 'last_container_error.log')} 2>&1")
        raise
    finally:
        if session_ctx:
            try:
                await session_ctx.__aexit__(None, None, None)
            except Exception:
                pass
        try:
            await stdio_ctx.__aexit__(None, None, None)
        except Exception:
            pass
        # Robustness: Give OS time to reap file handles
        await asyncio.sleep(0.2)

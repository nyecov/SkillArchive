import os
import pytest
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

pytest_mark_asyncio_alias = pytest.mark.asyncio

WORKSPACE_ROOT = "g:/Skill Archive"

async def manual_server_boot(staging_dir):
    """Utility to boot the server and return the session for diagnostic checks."""
    lock_path = os.path.join(staging_dir, ".engine.instance.lock")

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "--init",
            "-v", f"{os.path.abspath(WORKSPACE_ROOT)}:/workspace",
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", "MEMORY_DIR=/workspace/temp__mem/Head/tests/staging",
            "context-engine-go:latest"
        ]
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                # Just do one call to ensure boot diagnostics ran
                await session.call_tool("read_session_state", {})
    except Exception:
        pass

@pytest_mark_asyncio_alias
async def test_diagnostics_detects_sqlite_corruption(test_workspace):
    """Verify that a corrupted engine.db triggers the PRAGMA integrity_check failure logged in diagnostics."""
    db_path = os.path.join(test_workspace, "engine.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    try:
        # 1. Create a dummy corrupted SQLite file BEFORE boot
        with open(db_path, "wb") as f:
            f.write(b"SQLite format 3\000 but the rest is complete garbage data to cause integrity check failure")
    
        lock_path = os.path.join(test_workspace, ".engine.instance.lock")

        server_params = StdioServerParameters(
            command="docker",
            args=[
                "run", "-i", "--rm", "--init",
                "-v", f"{os.path.abspath(WORKSPACE_ROOT)}:/workspace",
                "-e", "WORKSPACE_ROOT=/workspace",
                "-e", "MEMORY_DIR=/workspace/temp__mem/Head/tests/staging",
                "context-engine-go:latest"
            ]
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                res = await session.call_tool("read_session_state", {})
                
                assert res.isError
                assert "ToolError: Failed to init storage" in res.content[0].text
                assert "file is not a database" in res.content[0].text
    finally:
        # Cleanup to prevent polluting the next diagnostic test
        if os.path.exists(db_path):
            os.remove(db_path)

@pytest.mark.asyncio
async def test_diagnostics_logging(test_workspace):
    """Verify that diagnostics results are saved to engine_diagnostics.log."""
    log_path = os.path.join(test_workspace, "engine_diagnostics.log")
    
    # Ensure a boot has happened
    await manual_server_boot(test_workspace)
    
    assert os.path.exists(log_path)
    with open(log_path, "r") as f:
        log_content = f.read()
    
    assert "Starting Context Engine Boot Sequence" in log_content
    assert "Boot Sequence Complete" in log_content

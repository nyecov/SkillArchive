import os
import pytest
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

WORKSPACE_ROOT = "g:/Skill Archive"

async def manual_server_boot(staging_dir):
    """Utility to boot the server and return the session for diagnostic checks."""
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
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await asyncio.wait_for(session.initialize(), timeout=10.0)
            # Just do one call to ensure boot diagnostics ran
            await session.call_tool("read_session_state", {})
            return True

@pytest.mark.asyncio
async def test_diagnostics_quarantine_corrupted_json(test_workspace):
    """Verify that a corrupted JSON file is renamed to .corrupted-[timestamp] on boot."""
    scratch_path = os.path.join(test_workspace, "current_session.json")
    ontology_path = os.path.join(test_workspace, "ontology.json")
    
    # 1. Manually create corrupted files BEFORE boot
    for p in [scratch_path, ontology_path]:
        if os.path.exists(p):
            os.remove(p)
        with open(p, "w") as f:
            f.write("{ invalid_json: [")

    # 2. Boot the server manually
    await manual_server_boot(test_workspace)

    # 3. Verify physical state
    files = os.listdir(test_workspace)
    assert not os.path.exists(scratch_path)
    assert not os.path.exists(ontology_path)
    assert any(".corrupted-" in f and "current_session.json" in f for f in files)
    assert any(".corrupted-" in f and "ontology.json" in f for f in files)
    print("\n✅ Poka-yoke Verified: Corrupted Memory Tiers were successfully quarantined.")

@pytest.mark.asyncio
async def test_diagnostics_reject_manual_circumvention(test_workspace):
    """Verify that removing __uuid or __version triggers a quarantine (Circumvention Guard)."""
    scratch_path = os.path.join(test_workspace, "current_session.json")
    ontology_path = os.path.join(test_workspace, "ontology.json")
    
    # 1. Create "tampered" files missing metadata BEFORE boot
    tampered_data = {"findings": []}
    for p in [scratch_path, ontology_path]:
        with open(p, "w") as f:
            json.dump(tampered_data, f)

    # 2. Boot
    await manual_server_boot(test_workspace)

    # 3. Verify
    files = os.listdir(test_workspace)
    assert any(".corrupted-" in f and "current_session.json" in f for f in files)
    assert any(".corrupted-" in f and "ontology.json" in f for f in files)
    print("\n✅ Poka-yoke Verified: Manual circumvention was successfully detected across tiers.")

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

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_diag():
    # Use relative paths for portability
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staging_dir = os.path.join(base_dir, "testing/staging")
    
    # Path inside container (assuming workspace mapping)
    container_staging = "/workspace/context-engine/testing/staging"
    
    # Clean lock
    lock_path = os.path.join(staging_dir, ".engine.instance.lock")
    if os.path.exists(lock_path):
        os.remove(lock_path)

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-v", f"{os.path.abspath(os.path.join(base_dir, '../../'))}:/workspace",
            "-e", "WORKSPACE_ROOT=/workspace",
            "-e", f"MEMORY_DIR={container_staging}",
            "context-engine-go:latest"
        ]
    )

    print("Starting server...")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await asyncio.wait_for(session.initialize(), timeout=20.0)
                print("Server Initialized.")
                
                # List tools to see if they are registered
                res = await session.list_tools()
                print("\nRegistered Tools:")
                for t in res.tools:
                    print(f"- {t.name}")
                
                # Try a lifecycle call
                print("\nTesting log_session_finding...")
                await session.call_tool("log_session_finding", {"finding_text": "Check", "phase": "execution"})
                print("Logged.")
                
                print("\nTesting clear_session_state...")
                await session.call_tool("clear_session_state", {})
                print("Cleared.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_diag())

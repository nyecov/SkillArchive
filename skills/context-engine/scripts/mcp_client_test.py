import json
import subprocess
import time
import sys
import threading

def read_stderr(proc):
    for line in iter(proc.stderr.readline, ''):
        if line:
            print(f"SERVER_LOG: {line.strip()}", file=sys.stderr)

def send_rpc(proc, method, params, request_id):
    msg = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }
    dump = json.dumps(msg)
    print(f"SENDING: {dump}")
    proc.stdin.write(dump + "\n")
    proc.stdin.flush()
    
    # Simple line-by-line read for response
    # In a real MCP client, you'd handle notifications too
    while True:
        line = proc.stdout.readline()
        if not line:
            return None
        print(f"RECEIVED: {line.strip()}")
        data = json.loads(line)
        if "id" in data and data["id"] == request_id:
            return data
        # Ignore notifications for now

def main():
    cmd = ["docker", "exec", "-i", "context-engine-daemon", "/context-engine-server"]
    print(f"Connecting to MCP server...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    # Start stderr logger thread
    threading.Thread(target=read_stderr, args=(proc,), daemon=True).start()

    try:
        # 1. Initialize
        print("\n--- Phase 1: Initialize ---")
        init_resp = send_rpc(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }, 1)
        
        # Initialized notification
        notif = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        proc.stdin.write(json.dumps(notif) + "\n")
        proc.stdin.flush()

        # 2. Short-Term Memory
        print("\n--- Phase 2: Short-Term (Create/Delete/Modify) ---")
        # Create
        send_rpc(proc, "tools/call", {
            "name": "log_session_finding",
            "arguments": {"finding_text": "SCRATCH_TO_DELETE", "phase": "planning"}
        }, 2)
        # Modify (Add more context/Log follow-up)
        send_rpc(proc, "tools/call", {
            "name": "log_session_finding",
            "arguments": {"finding_text": "SCRATCH_PERSISTENT: Verification in progress.", "phase": "execution"}
        }, 3)
        # Delete
        send_rpc(proc, "tools/call", {
            "name": "delete_session_finding",
            "arguments": {"index": 0}
        }, 4)

        # 3. Middle-Term Memory (Create/Delete)
        print("\n--- Phase 3: Middle-Term (Create/Delete) ---")
        # Create
        send_rpc(proc, "tools/call", {
            "name": "commit_ontology_edge",
            "arguments": {"source_entity": "UI_Component", "edge_type": "REQUIRES", "target_entity": "Backend_API"}
        }, 5)
        # Create another to delete
        send_rpc(proc, "tools/call", {
            "name": "commit_ontology_edge",
            "arguments": {"source_entity": "Temp_Node", "edge_type": "REFERENCES", "target_entity": "Trash"}
        }, 6)
        # Delete
        send_rpc(proc, "tools/call", {
            "name": "delete_ontology_edge",
            "arguments": {"source_entity": "Temp_Node", "edge_type": "REFERENCES", "target_entity": "Trash"}
        }, 7)

        # 4. Long-Term Memory (Ingestion)
        print("\n--- Phase 4: Long-Term (Ingestion) ---")
        send_rpc(proc, "tools/call", {
            "name": "ingest_context",
            "arguments": {"target_path": "context-engine/SKILL.md"}
        }, 8)

        print("\n--- Test Sequence Finished ---")
        time.sleep(2)

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()

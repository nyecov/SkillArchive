import json
import subprocess
import time
import sys
import threading

def send_rpc(proc, method, params, request_id):
    msg = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }
    dump = json.dumps(msg)
    proc.stdin.write(dump + "\n")
    proc.stdin.flush()
    
    while True:
        line = proc.stdout.readline()
        if not line: return None
        data = json.loads(line)
        if "id" in data and data["id"] == request_id:
            return data

def main():
    cmd = ["docker", "exec", "-i", "context-engine-daemon", "/context-engine-server"]
    print("Connecting to cleanup server...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    try:
        # Initialize
        send_rpc(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "cleanup-client", "version": "1.0.0"}
        }, 1)
        
        notif = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        proc.stdin.write(json.dumps(notif) + "\n")
        proc.stdin.flush()

        # 1. Clear Scratchpad (Multi-level delete/clear)
        print("Clearing Scratchpad...")
        send_rpc(proc, "tools/call", {
            "name": "clear_session_state",
            "arguments": {}
        }, 2)

        # 2. Delete Ontology Edges
        # Based on previous tests: System -> Database, UI_Component -> Backend_API
        print("Deleting Ontology Edges...")
        edges = [
            ("System", "REQUIRES", "Database"),
            ("UI_Component", "REQUIRES", "Backend_API"),
            ("Backend_API", "REQUIRES", "Database"),
             ("ALPHA", "REQUIRES", "BETA")
        ]
        for s, e, t in edges:
            send_rpc(proc, "tools/call", {
                "name": "delete_ontology_edge",
                "arguments": {
                    "source_entity": s,
                    "edge_type": e,
                    "target_entity": t
                }
            }, 10)

        print("Cleanup sequence finished.")
        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()

import json
import os
import argparse
import subprocess
from pathlib import Path

# State file to track horizontal deployment
STATE_FILE = Path(".gemini/tmp/yokoten_state.json")

def load_state():
    if not STATE_FILE.exists():
        return {
            "pattern": "",
            "targets": [],
            "current_index": 0,
            "batches": [],
            "batch_size": 5,
            "retry_count": {},
            "status": "init" # init, scanning, deploying, completed, halted
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def start_scan(pattern, targets):
    state = load_state()
    state["pattern"] = pattern
    state["targets"] = targets
    state["current_index"] = 0
    state["status"] = "scanning"
    
    # Heijunka: Chunk targets into batches of 5
    state["batches"] = [targets[i:i + state["batch_size"]] for i in range(0, len(targets), state["batch_size"])]
    state["retry_count"] = {t: 0 for t in targets}
    
    save_state(state)
    print(f"Yokoten Scan Initialized. Found {len(targets)} targets. Batched into {len(state['batches'])} groups.")

def verify_target(target_path, test_command):
    """
    Jidoka: Deterministically verify the target file using local tests.
    """
    state = load_state()
    if target_path not in state["retry_count"]:
        state["retry_count"][target_path] = 0
        
    print(f"Verifying target: {target_path} using `{test_command}`")
    
    try:
        # Run the test command
        result = subprocess.run(test_command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"Verification PASS for {target_path}")
            return True
        else:
            state["retry_count"][target_path] += 1
            save_state(state)
            
            if state["retry_count"][target_path] >= 2:
                print(f"JIDOKA HALT: {target_path} failed verification twice. Manual intervention required.")
                state["status"] = "halted"
                save_state(state)
                return False
            
            print(f"Verification FAIL for {target_path} (Attempt {state['retry_count'][target_path]}). Agent may retry once.")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Verification TIMEOUT for {target_path}. Halting.")
        state["status"] = "halted"
        save_state(state)
        return False

def render_report():
    state = load_state()
    report = f"# Yokoten Deployment Report\n\n- **Pattern:** {state['pattern']}\n- **Status:** {state['status']}\n\n## Target Status\n"
    
    for target in state["targets"]:
        retries = state["retry_count"].get(target, 0)
        report += f"- {target}: {'[HALTED]' if state['status'] == 'halted' and retries >= 2 else '[PENDING]' if retries == 0 else '[VERIFIED]' if retries < 2 else '[FAILED]'}\n"
        
    print(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Yokoten Batch Controller")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    scan_parser = subparsers.add_parser("scan", help="Initialize scan and batching")
    scan_parser.add_argument("pattern", help="The code pattern being broadcast")
    scan_parser.add_argument("targets", nargs="+", help="List of target file paths")
    
    verify_parser = subparsers.add_parser("verify", help="Verify a target file after update")
    verify_parser.add_argument("path", help="Path to the file to verify")
    verify_parser.add_argument("--test", required=True, help="Test command to run")
    
    subparsers.add_parser("report", help="Render the Deployment Report")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        start_scan(args.pattern, args.targets)
    elif args.command == "verify":
        success = verify_target(args.path, args.test)
        if not success:
            exit(1)
    elif args.command == "report":
        render_report()

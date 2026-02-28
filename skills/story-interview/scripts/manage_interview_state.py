import json
import os
import argparse
from pathlib import Path

# The state file will be stored in the temporary agent workspace
STATE_FILE = Path(".gemini/tmp/current_interview_state.json")

def load_state():
    if not STATE_FILE.exists():
        return {
            "current_phase": "init",
            "story_name": "",
            "user_value": "",
            "core_logic": "",
            "edge_cases": [],
            "verification_criteria": [],
            "unresolved_questions": []
        }
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("KYT WARNING: State file corrupted. Graceful degradation to conversational mode required.")
        return None

def save_state(state):
    # Ensure directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"State saved successfully to {STATE_FILE}.")

def init_interview():
    state = {
        "current_phase": "defining_value",
        "story_name": "",
        "user_value": "",
        "core_logic": "",
        "edge_cases": [],
        "verification_criteria": [],
        "unresolved_questions": []
    }
    save_state(state)
    print("Interview State Initialized. Phase: defining_value")

def update_field(field, value, is_list=False):
    state = load_state()
    if state is None: return

    if is_list:
        if field not in state or not isinstance(state[field], list):
            state[field] = []
        state[field].append(value)
    else:
        state[field] = value
    
    save_state(state)

def advance_phase(new_phase):
    valid_phases = ["init", "defining_value", "interrogating_logic", "probing_edge_cases", "ready_for_consensus"]
    if new_phase not in valid_phases:
        print(f"Error: Invalid phase '{new_phase}'")
        return
    
    state = load_state()
    if state is None: return

    state["current_phase"] = new_phase
    save_state(state)
    print(f"Phase advanced to: {new_phase}")

def render_output():
    state = load_state()
    if state is None: return
    
    if state["current_phase"] != "ready_for_consensus":
        print(f"Error: Cannot render output. Current phase is {state['current_phase']}, expected 'ready_for_consensus'.")
        return
        
    template = f"""
# Development Story: {state.get('story_name', '[Concise Name]')}

## 1. User Value (Why)
{state.get('user_value', '[The specific problem being solved and for whom.]')}

## 2. Core Logic (How)
{state.get('core_logic', '[The technical approach and behavior agreed upon.]')}

## 3. Edge Cases & Constraints
"""
    for edge in state.get('edge_cases', []):
        template += f"- {edge}\n"
        
    template += "\n## 4. Verification Criteria\n"
    for crit in state.get('verification_criteria', []):
        template += f"- [ ] {crit}\n"
        
    print("\n========= POKA-YOKE RENDERED OUTPUT =========\n")
    print(template)
    print("\n=============================================\n")

def print_state():
    state = load_state()
    if state is None: return
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the Story Interview deterministic state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    subparsers.add_parser("init", help="Initialize a new interview state")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a specific field in the state")
    update_parser.add_argument("field", help="The field to update (e.g., user_value, edge_cases)")
    update_parser.add_argument("value", help="The value to set or append")
    update_parser.add_argument("--list", action="store_true", help="If set, appends the value to an array rather than overwriting")

    # Advance command
    advance_parser = subparsers.add_parser("advance", help="Advance the interview to the next phase")
    advance_parser.add_argument("phase", help="The new phase (e.g., interrogating_logic, ready_for_consensus)")

    # Render command
    subparsers.add_parser("render", help="Render the final Poka-yoke Output Template from the current state")

    # View command
    subparsers.add_parser("view", help="View the current raw JSON state")

    args = parser.parse_args()

    # Create root directory path relative to CWD if needed, but the script expects CWD to be the workspace root
    # when invoked by the agent.
    
    if args.command == "init":
        init_interview()
    elif args.command == "update":
        update_field(args.field, args.value, args.list)
    elif args.command == "advance":
        advance_phase(args.phase)
    elif args.command == "render":
        render_output()
    elif args.command == "view":
        print_state()

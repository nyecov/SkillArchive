import subprocess
import sys

def run_test(command):
    """Runs the provided test command and returns True if it passes (exit code 0)."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def binary_search(items, test_command):
    """
    Performs a binary search over a list of items (e.g., lines, commits).
    The 'items' list must be ordered such that it starts 'working' and ends 'broken'.
    """
    low = 0
    high = len(items) - 1
    last_working_idx = -1

    print(f"Starting binary search over {len(items)} items...")

    while low <= high:
        mid = (low + high) // 2
        print(f"  Testing at index {mid} ({items[mid]})...", end=" ")
        
        # In a real scenario, you'd apply the state for 'items[mid]' here.
        # This script assumes the user provides a command that can test a specific state.
        if run_test(test_command.replace("{item}", str(items[mid]))):
            print("PASS")
            last_working_idx = mid
            low = mid + 1
        else:
            print("FAIL")
            high = mid - 1

    if last_working_idx != -1 and last_working_idx < len(items) - 1:
        print(f"
ISOLATED: The boundary is between index {last_working_idx} and {last_working_idx + 1}.")
        print(f"  Last Working: {items[last_working_idx]}")
        print(f"  First Broken: {items[last_working_idx + 1]}")
    else:
        print("
COULD NOT ISOLATE: Ensure the range starts working and ends broken.")

if __name__ == "__main__":
    # Example usage: python binary_search_runner.py "test_cmd {item}" item1 item2 item3...
    if len(sys.argv) < 3:
        print("Usage: python binary_search_runner.py <test_command_with_{item}> <item1> <item2> ...")
        sys.exit(1)
    
    test_cmd = sys.argv[1]
    items_to_test = sys.argv[2:]
    binary_search(items_to_test, test_cmd)

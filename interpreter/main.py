import argparse
import json
import os
from interpreter import ensure_binary_path

# Path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_STATE = {
    "initialized": False,
    "last_operation": None,
    "finished_last": False  # Tracks if 'finish' was the last operation
}

def load_state():
    """Load state from config.json, initializing it with default values if necessary."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                state = json.load(f)
        except json.JSONDecodeError:
            print("Warning: config.json is corrupted. Reinitializing with default state.")
            state = DEFAULT_STATE
    else:
        state = DEFAULT_STATE

    # Ensure all required keys are present
    for key, value in DEFAULT_STATE.items():
        if key not in state:
            state[key] = value

    # Save state to ensure the file exists with default values
    save_state(state)
    return state

def save_state(state):
    """Save state to config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(state, f, indent=4)

def suppress_output(silent_flags):
    """Suppress output based on silent flags."""
    if silent_flags["truesilent"]:
        return True  # Suppress all output
    return False

def main():
    # Get binary path (ensures it exists)
    binary_path = ensure_binary_path()

    # Load current state
    state = load_state()

    # Argument parser setup
    parser = argparse.ArgumentParser(description="CLI tool with binary path validation and operation constraints.")

    # Positional argument for the operation
    parser.add_argument(
        "operation",
        choices=["initialize", "forward", "finish", "terminate", "dump"],
        help="The operation to perform: initialize, forward, finish, terminate, or dump."
    )

    # Single-dash flags for dumping specific system states
    parser.add_argument("-r", action="store_true", help="Dump registers to console.")
    parser.add_argument("-m", action="store_true", help="Dump memory to console.")
    parser.add_argument("-l", action="store_true", help="Dump labels to console.")
    parser.add_argument("-s", action="store_true", help="Dump stack to console.")
    parser.add_argument("-f", action="store_true", help="Dump flags to console.")
    parser.add_argument("-p", action="store_true", help="Dump program data to console.")

    # Silent flags
    parser.add_argument("--silentc", action="store_true", help="Suppress compiler errors.")
    parser.add_argument("--silenti", action="store_true", help="Suppress interpreter module errors.")
    parser.add_argument("--silents", action="store_true", help="Suppress runtime errors.")
    parser.add_argument("--truesilent", action="store_true", help="Suppress all output, error or otherwise.")

    # Optional argument for the program file (used only in initialize)
    parser.add_argument(
        "--file",
        type=str,
        help="Path to the program file (required for 'initialize').",
        required=False
    )

    # Parse arguments
    args = parser.parse_args()

    # Collect silent flags into a dictionary for easier management
    silent_flags = {
        "silentc": args.silentc,
        "silenti": args.silenti,
        "silents": args.silents,
        "truesilent": args.truesilent,
    }

    if suppress_output(silent_flags):
        # Suppress all output
        return

    # Enforce constraints
    if args.operation == "initialize":
        if state["initialized"]:
            if not args.silenti:
                print("Error: Cannot initialize. A file is already initialized. Run 'terminate' first.")
            exit(1)
        if not args.file:
            if not args.silenti:
                print("Error: The 'initialize' operation requires a program file path (use --file).")
            exit(1)
        # Reset state for a new initialization
        state.update({
            "initialized": True,
            "last_operation": "initialize",
            "finished_last": False
        })
        save_state(state)
        print(f"Initialized program '{args.file}' with compiler binary '{binary_path}'")

    elif args.operation in ["forward", "finish", "dump"]:
        if not state["initialized"]:
            if not args.silenti:
                print(f"Error: Cannot run '{args.operation}' without initializing a file first.")
            exit(1)

        # Handle specific operations
        if args.operation == "forward":
            if state["finished_last"]:
                if not args.silenti:
                    print("Error: Cannot run 'forward' after 'finish'. Run 'terminate' first.")
                exit(1)
            state["last_operation"] = "forward"
            print(f"Executing 'forward' using compiler binary '{binary_path}'")

        elif args.operation == "finish":
            state.update({
                "last_operation": "finish",
                "finished_last": True
            })
            print(f"Executing 'finish' using compiler binary '{binary_path}'")

        elif args.operation == "dump":
            print("Dumping system state:")
            if args.r:
                print("Registers: [example register data]")
            if args.m:
                print("Memory: [example memory data]")
            if args.l:
                print("Labels: [example label data]")
            if args.s:
                print("Stack: [example stack data]")
            if args.f:
                print("Flags: [example flags data]")
            if args.p:
                print("Program Data: [example program state]")

        save_state(state)

    elif args.operation == "terminate":
        if not state["initialized"]:
            if not args.silenti:
                print("Error: Cannot terminate. No file has been initialized.")
            exit(1)
        # Reset state after termination
        state.update({
            "initialized": False,
            "last_operation": "terminate",
            "finished_last": False
        })
        save_state(state)
        print("System terminated. Ready to initialize a new file.")

if __name__ == "__main__":
    main()

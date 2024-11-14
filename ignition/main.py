import argparse
import json
import os
from ignition import ensure_binary_path

# Path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# Default state
DEFAULT_STATE = {
    "initialized": False,
    "last_operation": None,
    "finished_last": False,
    "current_file": None,
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

    return state


def save_state(state):
    """Save state to config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(state, f, indent=4)


def suppress_output(silent_flags):
    """Suppress output based on silent flags."""
    return silent_flags.get("truesilent", False)


def process_command(state, args, silent_flags):
    """Process a single command based on the arguments."""
    if suppress_output(silent_flags):
        return state

    operation = args.operation

    # Enforce operation order constraints
    if operation == "initialize":
        if state["initialized"]:
            if not silent_flags["silenti"]:
                print(f"Error: Cannot initialize '{args.file}' as '{state['current_file']}' is already initialized. Run 'terminate' first to stop execution of the current program.")
            return state

        if not args.file:
            if not silent_flags["silenti"]:
                print("Error: The 'initialize' operation requires a .sasm program file path (use --file).")
            return state

        # Reset state for a new initialization
        state.update({
            "initialized": True,
            "last_operation": "initialize",
            "finished_last": False,
            "current_file": args.file,
        })
        print(f"Initialized program '{args.file}'.")

    elif operation in ["forward", "finish", "dump"]:
        if not state["initialized"]:
            if not silent_flags["silenti"]:
                print(f"Error: Cannot run '{operation}' without initializing a .sasm program first.")
            return state

        if operation == "forward":
            if state["finished_last"]:
                if not silent_flags["silenti"]:
                    print(f"Error: '{state['current_file']}' is at end of execution. Run 'terminate' first to release the current program.")
                return state
            state["last_operation"] = "forward"
            print(f"Executing 'forward' on program '{state['current_file']}'.")

        elif operation == "finish":
            if state["finished_last"]:
                if not silent_flags["silenti"]:
                    print(f"Error: '{state['current_file']}' is at end of execution. Run 'terminate' first to release the current program.")
                return state
            state.update({
                "last_operation": "finish",
                "finished_last": True,
            })
            print(f"Executing 'finish' on program '{state['current_file']}'.")

        elif operation == "dump":
            if not any([args.r, args.m, args.l, args.s, args.f, args.p]):
                print("Error: No attributes chosen to dump. Run '--help' for available flags.")
                return state
            print(f"Dumping system state for program '{state['current_file']}':")
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

    elif operation == "terminate":
        if not state["initialized"]:
            if not silent_flags["silenti"]:
                print("Error: Cannot terminate. No .sasm program has been initialized.")
            return state

        print(f"Terminated program '{state['current_file']}'")
        state.update({
            "initialized": False,
            "last_operation": "terminate",
            "finished_last": False,
            "current_file": None,
        })
        print("Ready to initialize a new .sasm program.")

    elif operation == "end":
        if state["initialized"]:
            print("Warning: Program is still initialized. Running 'terminate' before exiting.")
            # Perform termination
            print(f"Terminated program '{state['current_file']}'")
            state.update({
                "initialized": False,
                "last_operation": "terminate",
                "finished_last": False,
                "current_file": None,
            })
            save_state(state)  # Save the state after terminating

        print("Exiting the interpreter.")
        exit(0)

    return state


def main():
    # Get binary path (ensures it exists)
    binary_path = ensure_binary_path()

    # Parse the initial command
    parser = argparse.ArgumentParser(description="Ignition: The StartASM interpreter and step-through debugger.")
    parser.add_argument(
        "command",
        choices=["start"],
        help="Command to start the interpreter loop."
    )
    args = parser.parse_args()

    # Ensure the user provided the 'start' command
    if args.command != "start":
        print("Error: You must provide the 'start' command to begin.")
        exit(1)

    # Load initial state
    state = load_state()

    # Main loop for processing commands
    while True:
        # Argument parser setup for operations
        parser = argparse.ArgumentParser(description="Enter a command for the interpreter.")
        parser.add_argument(
            "operation",
            choices=["initialize", "forward", "finish", "terminate", "dump", "end"],
            help="The interpreter operation to perform."
        )
        parser.add_argument("-r", action="store_true", help="Dump registers to console.")
        parser.add_argument("-m", action="store_true", help="Dump memory to console.")
        parser.add_argument("-l", action="store_true", help="Dump labels to console.")
        parser.add_argument("-s", action="store_true", help="Dump stack to console.")
        parser.add_argument("-f", action="store_true", help="Dump flags to console.")
        parser.add_argument("-p", action="store_true", help="Dump program data to console.")
        parser.add_argument("--silentc", action="store_true", help="Suppress compiler errors.")
        parser.add_argument("--silenti", action="store_true", help="Suppress interpreter module errors.")
        parser.add_argument("--silents", action="store_true", help="Suppress runtime errors.")
        parser.add_argument("--truesilent", action="store_true", help="Suppress all output, including errors")
        parser.add_argument("--file", type=str, help="Path to the .sasm program file (used with 'initialize').")

        # Prompt user for input
        user_input = input("Enter command: ").strip().split()
        if not user_input:
            continue

        # Parse arguments
        try:
            args = parser.parse_args(user_input)
        except SystemExit:
            continue

        # Collect silent flags into a dictionary for easier management
        silent_flags = {
            "silentc": args.silentc,
            "silenti": args.silenti,
            "silents": args.silents,
            "truesilent": args.truesilent,
        }

        # Process the command
        state = process_command(state, args, silent_flags)

        # Save state after every command
        save_state(state)


if __name__ == "__main__":
    main()

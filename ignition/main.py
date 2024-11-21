import argparse
import json
import os
from ignition import ensure_docker_image
from ignition.interpreter import Interpreter

# Path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# Default state
DEFAULT_STATE = {
    "initialized": False,
    "last_operation": None,
    "current_file": None,
    "silent_flags": {
        "silentc": False,
        "silenti": False,
        "silentr": False,
        "truesilent": False,
    }
}


def load_state():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                state = json.load(f)
        except json.JSONDecodeError:
            print("Usage Warning: config.json is corrupted. Reinitializing with default state.")
            state = DEFAULT_STATE
    else:
        state = DEFAULT_STATE

    # Ensure all required keys are present
    for key, value in DEFAULT_STATE.items():
        if key not in state:
            state[key] = value

    return state


def save_state(state):
    with open(CONFIG_FILE, "w") as f:
        json.dump(state, f, indent=4)


def process_command(state, args, interpreter):
    operation = args.operation
    if operation == "initialize":
        if state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print(f"Usage Error: Cannot initialize '{args.file}'. '{state['current_file']}' is already initialized. Run 'terminate' first to stop execution of the current program.")
            return state

        if not args.file:
            if not state["silent_flags"]["silenti"]:
                print("Usage Error: The 'initialize' operation requires a .sasm program file path (use --file).")
            return state

        success = interpreter.initialize(args.file)  # Call interpreter.initialize
        if success:
            state.update({
                "initialized": True,
                "last_operation": "initialize",
                "current_file": args.file,
            })
        else:
            if not state["silent_flags"]["silenti"]:
                print(f"Usage Error: Initialization failed for program '{args.file}'. Terminating.")
            interpreter.terminate()  # Implicitly terminate
            state.update({  # Update the state to reflect termination
                "initialized": False,
                "last_operation": "terminate",
                "current_file": None,
            })

    elif operation == "restart":
        if not state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print("Usage Error: Cannot restart. No .sasm program has been initialized.")
            return state

        interpreter.restart()  # Call interpreter.restart
        # Reset the state to allow further operations
        state.update({
            "last_operation": "restart",
        })

    elif operation in ["forward", "run", "dump"]:
        if not state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print(f"Usage Error: Cannot run. No .sasm program is initialized.")
            return state

        if operation == "forward":
            num_steps = args.steps or 1  # Default to 1 if no steps are provided
            state["last_operation"] = "forward"
            try:
                interpreter.forward(num_steps)
            except:
                if not state["silent_flags"]["silenti"]:
                    print("Python Error. Unexpected runtime exception encountered. Running 'terminate'.")
                state.update({
                    "initialized": False,
                    "last_operation": "terminate",
                    "current_file": None,
                })
                interpreter.terminate()
                save_state(state)

        elif operation == "run":
            state.update({
                "last_operation": "run",
            })
            try:
                interpreter.finish()
            except:
                if not state["silent_flags"]["silenti"]:
                    print("Python Error. Unexpected runtime exception encountered. Running 'terminate'.")
                state.update({
                    "initialized": False,
                    "last_operation": "terminate",
                    "current_file": None,
                })
                interpreter.terminate()
                save_state(state)

        elif operation == "dump":
            if not any([args.r, args.m, args.s, args.f, args.p]):
                if not state["silent_flags"]["silenti"]:
                    print("Usage Error: No attributes chosen to dump. Run '--help' for available flags.")
                return state
            interpreter.dump(args.r, args.m, args.s, args.f, args.p, args.verbose)

    elif operation == "terminate":
        if not state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print("Usage Error: Cannot terminate. No .sasm program has been initialized.")
            return state

        state.update({
            "initialized": False,
            "last_operation": "terminate",
            "current_file": None,
        })
        interpreter.terminate()

    elif operation == "breakpoint":
        if not state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print("Usage Error: Cannot manage breakpoints. No .sasm program has been initialized.")
            return state
        if args.set is not None:
            line_num = args.set
            interpreter.set_breakpoint(line_num)  # Set a breakpoint at the specified line
        elif args.remove is not None:
            line_num = args.remove
            interpreter.remove_breakpoint(line_num)  # Remove the breakpoint at the specified line
        elif args.list:
            interpreter.list_breakpoints()  # List all breakpoints
        else:
            if not state["silent_flags"]["silenti"]:
                print("Usage Error: You must specify either --set, --remove, or --list.")

    elif operation == "end":
        if state["initialized"]:
            if not state["silent_flags"]["silenti"]:
                print("Warning: Program is still initialized. Running 'terminate' before exiting.")
            state.update({
                "initialized": False,
                "last_operation": "terminate",
                "current_file": None,
            })
            interpreter.terminate()
            save_state(state)  # Save the state after terminating
        exit(0)

    return state


def main():
    # Get Docker image (ensures it exists)
    compiler_image = ensure_docker_image()

    # Parse the initial command
    parser = argparse.ArgumentParser(description="Ignition: The StartASM interpreter and step-through debugger.")
    parser.add_argument(
        "command",
        choices=["start"],
        help="Command to start the interpreter loop."
    )
    parser.add_argument("--silentc", action="store_true", help="suppress StartASM Compiler errors.")
    parser.add_argument("--silenti", action="store_true", help="suppress Ignition usage errors.")
    parser.add_argument("--silentr", action="store_true", help="suppress StartASM runtime errors.")
    parser.add_argument("--truesilent", action="store_true", help="suppress all output, including errors")
    args = parser.parse_args()

    # Ensure the user provided the 'start' command
    if args.command != "start":
        print("Usage Error: You must provide the 'start' command to begin.")
        exit(1)

    # Initialize silent flags in state
    state = load_state()
    state["silent_flags"] = {
        "silentc": args.silentc,
        "silenti": args.silenti,
        "silentr": args.silentr,
        "truesilent": args.truesilent,
    }
    if state["silent_flags"]["truesilent"]:
        state["silent_flags"]["silentc"] = True
        state["silent_flags"]["silenti"] = True
        state["silent_flags"]["silentr"] = True
    save_state(state)

    interpreter = Interpreter(compiler_image, state["silent_flags"]["silenti"], state["silent_flags"]["silentc"], state["silent_flags"]["silentr"], state["silent_flags"]["truesilent"])

    # Main loop for processing commands
    while True:
        # Argument parser setup for operations
        parser = argparse.ArgumentParser(description="Enter a command for the interpreter.")
        parser.add_argument(
            "operation",
            choices=["initialize", "restart", "forward", "run", "terminate", "dump", "breakpoint", "end"],
            help="The interpreter operation to perform."
        )
        parser.add_argument("-r", action="store_true", help="dump registers to console.")
        parser.add_argument("-m", action="store_true", help="dump memory to console.")
        parser.add_argument("-s", action="store_true", help="dump stack to console.")
        parser.add_argument("-f", action="store_true", help="dump flags to console.")
        parser.add_argument("-p", action="store_true", help="dump program data to console.")
        parser.add_argument("--verbose", action="store_true", help="provide verbose output (used with 'dump') ")  # Add verbose flag
        parser.add_argument("--file", type=str, help="path to the .sasm program file (used with 'initialize').")
        parser.add_argument("--steps", type=int, help="number of steps to move forward (used with 'forward').")  # Add steps argument
        parser.add_argument("--set", type=int, help="set a breakpoint at the specified line number (used with 'breakpoint').")
        parser.add_argument("--remove", type=int, help="remove the breakpoint at the specified line number (used with 'breakpoint').")
        parser.add_argument("--list", action="store_true", help="list all active breakpoints (used with 'breakpoint').")

        # Prompt user for input
        user_input = input("> ").strip().split()
        if not user_input:
            continue

        # Parse arguments
        try:
            args = parser.parse_args(user_input)
        except SystemExit:
            continue

        # Process the command
        state = process_command(state, args, interpreter)

        # Save state after every command
        save_state(state)

if __name__ == "__main__":
    main()

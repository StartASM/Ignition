import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def get_config():
    """Load configuration from config.json."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save configuration to config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def validate_path(path):
    """Check if the provided binary path is valid."""
    return os.path.isfile(path) and os.access(path, os.X_OK)


def ensure_binary_path():
    """Ensure a valid binary path is set in the config."""
    config = get_config()
    binary_path = config.get("binary_path")

    if binary_path and validate_path(binary_path):
        return binary_path  #Binary path already set and valid

    print("No valid binary path found.")
    while True:
        binary_path = input("Please enter the full path to your C++ binary: ").strip()
        if validate_path(binary_path):
            config["binary_path"] = binary_path
            save_config(config)
            print(f"Binary path saved: {binary_path}")
            return binary_path
        else:
            print("Invalid path. Ensure the file exists and is executable.")


#Ensure binary path is set at the first import
ensure_binary_path()

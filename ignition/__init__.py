import os
import json
import subprocess

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


def validate_docker_image(image_name):
    """Check if the provided Docker image exists locally."""
    try:
        result = subprocess.run(
            ["docker", "images", "-q", image_name],
            text=True,
            capture_output=True,
            check=True
        )
        return bool(result.stdout.strip())
    except FileNotFoundError:
        print("Docker is not installed or not in PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking Docker images: {e}")
        return False


def ensure_docker_image():
    """Ensure a valid Docker image is set in the config."""
    config = get_config()
    docker_image = config.get("docker_image")

    if docker_image and validate_docker_image(docker_image):
        return docker_image  # Docker image already set and valid

    print("No valid Docker image found.")
    while True:
        docker_image = input("Please enter the full name of your StartASM Docker Image: ").strip()
        if validate_docker_image(docker_image):
            config["docker_image"] = docker_image
            save_config(config)
            print(f"Docker image saved: {docker_image}")
            return docker_image
        else:
            print("Invalid Docker image. Ensure the image exists locally and try again.")


# Ensure Docker image is set at the first import
ensure_docker_image()

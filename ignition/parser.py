import subprocess
import json

class Parser:
    def __init__(self):
        self.json_output = None

    def parse_program(self, program_path, compiler_image):
        self._call_compiler(program_path, compiler_image)
        return self.json_output

    def _call_compiler(self, program_path, compiler_image):
        compiler_command = ["docker", "run", "--rm", compiler_image, "ast", program_path]
        try:
            result = subprocess.run(
                compiler_command,
                text=True,
                capture_output=True,
                check=False
            )
            if result.returncode != 0:
                print(f"{result.stderr.strip()}")
                return None
            self.json_output = json.loads(result.stdout)

        except Exception as e:
            print(f"Failed to call compiler image: {str(e)}")
            return None


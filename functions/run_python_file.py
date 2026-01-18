import os, subprocess
from typing import Text


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_directory_abs_path, os.path.normpath(file_path))
        )
        valid_path = (
            os.path.commonpath([working_directory_abs_path, target_path])
            == working_directory_abs_path
        )
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(args)
        sub_process = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=30,
        )
        output = ""
        if sub_process.returncode != 0:
            output += f"Process exited with code {sub_process.returncode}\n"
        if not sub_process.stdout and not sub_process.stderr:
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {sub_process.stdout}\nSTDERR: {sub_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

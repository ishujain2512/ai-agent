import os, subprocess
from google.genai import types


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


schema_run_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory, providing STDOUT and STDERR from python subprocess",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to run file from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Option, Array of arguments to pass to the python file. each element of the array is a string literal",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="String element representing the argument to be passed to the python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)

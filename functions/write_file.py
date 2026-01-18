import os
from google.genai import types


def write_file(working_directory, file_path, content):
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file, given file relative to the working directory, providing a Successfully wrote to file message",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write contents to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents of files that are to be written, accepts contents as string properly formatted.",
            ),
        },
        required=["file_path", "content"],
    ),
)

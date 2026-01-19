import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_directory_abs_path, directory)
        )
        valid_target_dir = (
            os.path.commonpath(([working_directory_abs_path, target_path]))
            == working_directory_abs_path
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        listings = os.listdir(target_path)
        if not listings:
            return f"Error: Failed to read {target_path}"

        for listing in listings:
            listing_path = os.path.join(target_path, listing)
            print(
                f"- {listing}: file_size={os.path.getsize(listing_path)} bytes, is_dir={os.path.isdir(listing_path)}"
            )
        return listings
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

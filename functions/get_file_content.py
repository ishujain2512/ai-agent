import os

from config import MAX_CHAR


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_dir_abs_path, os.path.normpath(file_path))
        )
        valid_dir = (
            os.path.commonpath([working_dir_abs_path, target_path])
            == working_dir_abs_path
        )
        if not valid_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHAR)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

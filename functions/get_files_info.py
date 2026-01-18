import os


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

    except Exception as e:
        return f"Error: {e}"

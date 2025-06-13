import os
from google.generativeai import types as gg_types # Updated import
import copy


def get_file_content(working_directory, file_path):
    """
    Gets the content of a file, constrained to the working directory.

    Args:
        working_directory: The working directory.
        file_path: The path to the file, relative to the working directory.

    Returns:
        The content of the file, or an error message if the file could not be read.
    """
    MAX_CHARS = 10000

    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs,file_path))

    if not target_file.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # print(f"DEBUG: working_dir: {working_dir_abs}")
    # print(f"DEBUG: target_file: {target_file}")
    # print(f"DEBUG: starts with test: {target_file.startswith(working_dir_abs)}")

    
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f"Error: could not read file: {e}"

schema_get_file_content = gg_types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file, constrained to the working directory.",
    parameters=copy.deepcopy({ # Pass as a dictionary, ensure deepcopy
        "type": "object", # Use string value
        "properties": {
            "file_path": {
                "type": "string", # Use string value
                "description": "The path to the file, relative to the working directory.",
            },
        },
        "required": ["file_path"],
    })
)
# Removed main() and if __name__ == "__main__": block (was already removed in previous step)

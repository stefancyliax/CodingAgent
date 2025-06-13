import os
from google.generativeai import types as gg_types # Updated import
import copy


def get_files_info(working_directory, directory=None):
    """
    Lists files in the specified directory along with their sizes, constrained to the working directory.

    Args:
        working_directory: The working directory.
        directory: The directory to list files from, relative to the working directory. If None, lists files in the working directory itself.

    Returns:
        A string containing the list of files and their sizes, or an error message if the directory could not be listed.
    """
    
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_dir_abs,directory or ""))

    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    
    file_list = os.listdir(target_dir)

    try:
        if file_list:
            return_str = ""
            for file in file_list:
                return_str += f"- {file}: file_size={os.path.getsize(os.path.join(target_dir, file))}, is_dir={os.path.isdir(os.path.join(target_dir, file))}\n"
            return return_str
        else: 
            return "no files found"
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = gg_types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=copy.deepcopy({ # Pass as a dictionary, ensure deepcopy
        "type": "object", # Use string value
        "properties": {
            "directory": {
                "type": "string", # Use string value
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            },
        },
        # No "required" field for this schema
    })
)
# Removed main() and if __name__ == "__main__": block (was already removed in previous step)

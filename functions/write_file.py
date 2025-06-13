import os
from google.generativeai import types as gg_types # Updated import
import copy

def write_file(working_directory, file_path, content):
    """
    Writes content to a file, constrained to the working directory.

    Args:
        working_directory: The working directory.
        file_path: The path to the file, relative to the working directory.
        content: The content to write to the file.

    Returns:
        A message indicating success or failure.
    """
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs,file_path))

    if not target_file.startswith(working_dir_abs):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    # print(f"DEBUG: working_dir: {working_dir_abs}")
    # print(f"DEBUG: target_file: {target_file}")
    # print(f"DEBUG: target_dir: {target_file}")
    
    # print(f"DEBUG: starts with test: {target_file.startswith(working_dir_abs)}")
    if os.path.exists(target_file) and os.path.isdir(target_file):
        return f'Error: "{file_path}" is a directory, not a file'

    if not os.path.exists(os.path.dirname(target_file)):
        try:
            os.makedirs(os.path.dirname(target_file))
        except Exception as e:
            return f"Error: could not create file {target_file} with {e}"
        #return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: could not write file: {e}"

schema_write_file = gg_types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=copy.deepcopy({ # Apply deepcopy here
        "type": "object", # Use string literal "object"
        "properties": {
            "file_path": {
                "type": "string", # Use string literal "string"
                "description": "The path to the file, relative to the working directory."
            },
            "content": {
                "type": "string", # Use string literal "string"
                "description": "The content to write to the file."
            },
        },
        "required": ["file_path", "content"],
    })
)
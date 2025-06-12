import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path):

    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs,file_path))

    if not target_file.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    print(f"DEBUG: working_dir: {working_dir_abs}")
    print(f"DEBUG: target_file: {target_file}")
    print(f"DEBUG: target_dir: {target_file}")

    return_string = ""
    try: 
        print(f"running file {target_file}")
        result = subprocess.run(
            [sys.executable, target_file],
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Decode stdout/stderr as text (UTF-8 by default)
            check=True,            # Raise CalledProcessError if the command returns a non-zero exit code
            timeout=30
        )
        return_string += "\nSTDOUT:"
        return_string += result.stdout
        return_string += "\nSTDERR:"
        return_string += result.stderr
        if result.returncode != 0:
            return_string += f"\nExit code: {result.returncode}"
        if result is None:
            return "No output produced."
        return return_string
    except Exception as e:
        return f"Error: executing Python file: {target_file} with {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file, relative to the working directory.",
            ),
        },
    ),
)


    
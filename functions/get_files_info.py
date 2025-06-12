import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    
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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def main():
    print(get_files_info("../../","../"))

if __name__ == "__main__":
    main()

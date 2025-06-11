import os


def get_file_content(working_directory, file_path):
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


def main():
    print(get_file_content("../calculator","lorem.txt"))

if __name__ == "__main__":
    main()

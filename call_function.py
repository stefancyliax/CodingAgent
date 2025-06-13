from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.get_pdf_content import get_pdf_content, schema_get_pdf_content
from google.genai import types # Reverted import

working_directory = "./calculator"

available_functions = types.Tool( # Ensure this uses the reverted types
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_get_pdf_content,
        ]
    )

def call_function(function_call_part, verbose=False):
    """
    Calls the appropriate function based on the function_call_part.name.

    Args:
        function_call_part: The function call part from the Gemini response.
        verbose: Whether to print verbose output.

    Returns:
        A types.Content object containing the function response.
    """
    func_dict = {
        "get_files_info": lambda: get_files_info(working_directory=working_directory, **function_call_part.args),
        "get_file_content": lambda: get_file_content(working_directory=working_directory, **function_call_part.args),
        "run_python_file": lambda: run_python_file(working_directory=working_directory, **function_call_part.args),
        "write_file": lambda: write_file(working_directory=working_directory, **function_call_part.args),
        "get_pdf_content": lambda: get_pdf_content(working_directory=working_directory, **function_call_part.args) # New function entry
    }

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in func_dict:
        function_result = func_dict[function_call_part.name]()
        return types.Content( # Ensure this uses the reverted types
            role="tool",
            parts=[
                types.Part.from_function_response( # Ensure this uses the reverted types
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content( # Ensure this uses the reverted types
            role="tool",
            parts=[
                types.Part.from_function_response( # Ensure this uses the reverted types
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

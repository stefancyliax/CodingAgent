import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    VERBOSE = False 
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    print("Hello from codingagent!")

    
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        sys.exit(1)

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        if len(sys.argv) > 2:
            VERBOSE=True if sys.argv[2] == "--verbose" else False
    else:
        print('Please provide a prompt. e.g. python main.py "Why is this so hard?"')
        sys.exit(1)
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
    except Exception as e:
        print(f"Error generating content: {e}")
        sys.exit(1)

    if response:
        if VERBOSE:
            print(f"User prompt: {user_prompt}")
            if response.usage_metadata:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            else:
                print("Usage metadata not available.")
        print("Response:")
        print(response.text)

        # Check if the response contains a function call
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
            function_call_part = response.candidates[0].content.parts[0].function_call
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print("No function called.")



if __name__ == "__main__":
    main()

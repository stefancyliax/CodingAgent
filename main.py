import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import call_function

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


    if VERBOSE:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, VERBOSE)

        if not function_call_result.parts[0].function_response:
            raise Exception(f"Error: Function response empty")

        function_responses.append(function_call_result.parts[0])
        if VERBOSE:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    if not function_responses:
        raise Exception("no function responses generated, exiting.")



if __name__ == "__main__":
    main()

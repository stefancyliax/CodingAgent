import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import call_function,available_functions
import argparse

def main():
    """
    Main function to set up the AI coding agent, parse user prompts,
    initialize the Gemini client, generate content, and call functions based on the response.
    """
    # set up
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    VERBOSE = False 
    MAX_CALLS = 20
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    parser = argparse.ArgumentParser(description="A helpful AI coding agent.")
    parser.add_argument("prompt", help="The user prompt.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode.")

    args = parser.parse_args()

    user_prompt = args.prompt
    VERBOSE = args.verbose

        
    print("Hello from codingagent!")

    # Create LLM client with Gemini    
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        sys.exit(1)
    
    # Call LLM    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    calls = 0
    while True:
        calls += 1
        if calls > MAX_CALLS:
            print(f"Maximum number of calls ({MAX_CALLS}) reached.")
            sys.exit(1)
                

        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
                )
        except Exception as e:
            print(f"Error generating content: {e}")
            sys.exit(1)

        # Process response
        if VERBOSE:
            print(f"User prompt: {user_prompt}")
            if response.usage_metadata:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)


        if not response.function_calls:
            print(response.text)
            return
        else: 
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, VERBOSE)

                if not function_call_result.parts[0].function_response:
                    raise Exception(f"Error: Function response empty")

                function_responses.append(function_call_result.parts[0])
                if VERBOSE:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            if not function_responses:
                raise Exception("no function responses generated, exiting.")
        
            messages.append(types.Content(role="tool", parts=function_responses))

            




if __name__ == "__main__":
    main()


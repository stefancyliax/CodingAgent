import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    print("Hello from codingagent!")

    
    client = genai.Client(api_key=api_key)
    if len(sys.argv) > 2: 
        user_prompt = sys.argv[1]
        VERBOSE=True if sys.argv[2] == "--verbose" else False
    else:
        print('Please provide a prompt. e.g. python main.py "Why is this so hard?"')
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)

    if VERBOSE: 
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()

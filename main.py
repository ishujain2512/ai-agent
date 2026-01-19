import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Please Provide a Gemini Key; Ensure it is contained in the .env file."
    )


def generate_response(contents):
    model = "gemini-2.5-flash"
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError(
            "Failed to fetch response please check your network connection."
        )
    return response


def main():
    parser = argparse.ArgumentParser(description="Chatbot to help with code")
    parser.add_argument("user_prompt", type=str, help="Ask me Something")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(5):
        response = generate_response(messages)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            function_call_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=True)
                if not function_call_result.parts:
                    raise Exception("No parts in function call result")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function Response Object is None")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function Response is None")
                function_call_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

            messages.append(types.Content(role="user", parts=function_call_results))
        else:
            print(response.text)
            return
    print(
        "Error: The Chatbot has run out of iterations and has not yet been able to produce a good enough response please try again."
    )
    sys.exit(1)


main()

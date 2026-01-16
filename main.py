import argparse
import os
from dotenv import load_dotenv

from call_function import call_function, tools
from openai import OpenAI
from prompts import system_prompt

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("BASE_URL")
model_name = os.environ.get("MODEL_NAME")

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        messages, finished = generate_content(client, messages, args.verbose)

        if finished:
            break


def generate_content(client, messages, verbose):
    finished = False
    response = client.chat.completions.create(
        model=model_name,
        tools=tools,
        messages=messages,
        tool_choice="auto",
    )

    if verbose:
        print(f"Prompt tokens: {response.timings['prompt_n']}")
        print(f"Response tokens: {response.timings['predicted_n']}")
        print(f"Prompt tokens/sec: {response.timings['prompt_per_second']}")
        print(f"Response tokens/sec: {response.timings['predicted_per_second']}")

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        print(f"Model requested {len(tool_calls)} tool calls.")

        messages.append(response_message)

        for tool_call in tool_calls:
            messages.append(call_function(tool_call, verbose))

    if response.choices[0].finish_reason == "stop":
        finished = True


    print("Response")
    print(response.choices[0].message.content)

    return messages, finished



if __name__ == "__main__":
    main()

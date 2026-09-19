import argparse
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from texts import CORPUS, LANGUAGES


MODEL = "gemini-3.6-flash"
OUTPUT_PATH = "measurements.json"
MAX_OUTPUT_TOKENS = 2048


def count_request_tokens(client, model, system_prompt, user_text):
    combined_text = system_prompt + "\n\n" + user_text

    response = client.models.count_tokens(
        model=model,
        contents=combined_text
    )

    return response.total_tokens


def make_request(client, model, system_prompt, user_text):
    response = client.models.generate_content(
        model=model,
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS
        )
    )

    usage = response.usage_metadata

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    thoughts_tokens = usage.thoughts_token_count or 0
    total_tokens = usage.total_token_count

    print("\n" + "=" * 70)
    print("GEMINI RESPONSE")
    print("=" * 70)
    print(response.text)

    print("\nTOKEN USAGE")
    print(f"Input tokens:    {input_tokens}")
    print(f"Output tokens:   {output_tokens}")
    print(f"Thinking tokens: {thoughts_tokens}")
    print(f"Total tokens:    {total_tokens}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "thoughts_tokens": thoughts_tokens,
        "total_tokens": total_tokens,
        "answer": response.text,
    }


def main():
    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY not found. Check your .env file."
        )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--call",
        action="store_true",
        help="Make real Gemini API requests"
    )
    args = parser.parse_args()

    client = genai.Client()

    print(f"Model: {MODEL}")

    token_counts = {}
    request_tokens = {}
    one_request_billed = {}

    for lang in LANGUAGES:
        system_prompt = CORPUS["system_prompt"][lang]
        complaint = CORPUS["complaint"][lang]

        counted_tokens = count_request_tokens(
            client,
            MODEL,
            system_prompt,
            complaint
        )

        token_counts[lang] = counted_tokens
        request_tokens[lang] = counted_tokens

        print(
            f"{lang}: request input tokens = {counted_tokens}"
        )

    if args.call:
        for lang in LANGUAGES:
            system_prompt = CORPUS["system_prompt"][lang]
            complaint = CORPUS["complaint"][lang]

            print("\n" + "#" * 70)
            print(f"LANGUAGE: {lang}")
            print("#" * 70)

            result = make_request(
                client,
                MODEL,
                system_prompt,
                complaint
            )

            one_request_billed[lang] = {
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "thoughts_tokens": result["thoughts_tokens"],
                "total_tokens": result["total_tokens"],
            }

    output = {
        "provider": "Google Gemini API",
        "model": MODEL,
        "model_id": MODEL,
        "token_counts": token_counts,
        "request_tokens": request_tokens,
        "one_request_billed": one_request_billed,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"Saved results to {OUTPUT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()
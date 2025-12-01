import os
from dotenv import load_dotenv
from openai import OpenAI


MODEL = "gpt-4o"

def test_connection() -> None:
    """Test that the OpenAI API key loads and a simple request succeeds."""

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Missing OPENAI_API_KEY. Add it to your .env file before running this script.")
        return

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": "Write a Python function to calculate the Fibonacci sequence."},
            ],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Error calling OpenAI API: {exc}")
        return

    message = response.choices[0].message.content or ""
    print("Success! API Response:\n")
    print(message.strip())


def main() -> None:
    test_connection()


if __name__ == "__main__":
    main()

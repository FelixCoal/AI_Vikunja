from together import Together
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def get_client():
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY is not set")
    return Together(api_key=api_key)

def ask_together(question):
    client = get_client()
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[
        {
            "role": "user",
            "content": question
        }
        ]
    )

    try:
        response = response.choices[0].message.content
        return response
    except (IndexError, AttributeError) as e:
        print(f"Error processing response: {e}")
        return None
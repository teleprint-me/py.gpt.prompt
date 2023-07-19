import sys

import dotenv
import openai

path = ".env"

dotenv.load_dotenv(path)

openai.api_key = dotenv.get_key(path, "OPENAI_API_KEY")

chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "My name is ChatGPT. I am a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is your name?",
        },
    ],
    stream=True,
)

for packet in chat_completion:
    if packet.choices[0].delta:
        print(packet.choices[0].delta["content"], end="")
        sys.stdout.flush()
print()

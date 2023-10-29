"""
docs/notebooks/poc_llama_function_calling.py
"""
import json
from pprint import pprint
from typing import List, Union

import requests
from llama_cpp import ChatCompletionMessage, Llama, LlamaGrammar

# Define the path to the model
MODEL_PATH = "models/mistralai/Mistral-7B-Instruct-v0.1/ggml-model-f16.gguf"

# Initialize the Llama model
llm = Llama(model_path=MODEL_PATH, verbose=False)

# Load a grammar file
llama_grammar = LlamaGrammar.from_file("docs/notebooks/json.gbnf")

# Function definitions
FUNCTIONS = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["metric", "uscs"]},
            },
            "required": ["location"],
        },
    },
    {
        "name": "binary_arithmetic",
        "description": "Perform binary arithmetic operations on two operands.",
        "parameters": {
            "type": "object",
            "properties": {
                "left_op": {
                    "type": ["integer", "number"],
                    "description": "The left operand.",
                },
                "right_op": {
                    "type": ["integer", "number"],
                    "description": "The right operand.",
                },
                "operator": {
                    "type": "string",
                    "description": "The arithmetic operator. Supported operators are '+', '-', '*', '/', '%'.",
                    "enum": ["+", "-", "*", "/", "%"],
                },
            },
            "required": ["left_op", "right_op", "operator"],
        },
    },
]


def get_current_weather(location: str, unit: str = "metric") -> str:
    """
    Get the current weather in a given location.
    Parameters:
    location (str): The city and state, e.g. San Francisco, CA
    unit (str): The unit system, can be either 'metric' or 'uscs'. Default is 'metric'.
    Returns:
    str: A string that describes the current weather.
    """

    # Replace spaces with hyphens and commas with underscores for the wttr.in URL
    location = location.replace(" ", "-").replace(",", "_")

    # Determine the unit query parameter
    unit_query = "m" if unit == "metric" else "u"
    # Set the API response formatting
    res_format = "%l+%T+%S+%s+%C+%w+%t"

    # Make a request to the wttr.in service
    response = requests.get(
        f"http://wttr.in/{location}?{unit_query}&format={res_format}"
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Return the weather report
        return response.text
    else:
        return f"Could not get the weather for {location}."


def binary_arithmetic(
    left_op: Union[int, float], right_op: Union[int, float], operator: str
) -> Union[int, float]:
    """
    Perform binary arithmetic operations on two operands.

    Parameters:
    - left_op (int/float): The left operand.
    - right_op (int/float): The right operand.
    - operator (str): The arithmetic operator. Supported operators are '+', '-', '*', '/', '%'.

    Returns:
    - int/float: The result of the arithmetic operation.
    """
    if operator == "+":
        return left_op + right_op
    elif operator == "-":
        return left_op - right_op
    elif operator == "*":
        return left_op * right_op
    elif operator == "/":
        if right_op == 0:
            raise ValueError("Division by zero is not allowed.")
        return left_op / right_op
    elif operator == "%":
        return left_op % right_op
    else:
        raise ValueError(
            f"Unsupported operator '{operator}'. Supported operators are '+', '-', '*', '/', '%'."
        )


# Generate chat sequence
def generate_chat_sequence(
    user_query: str, function_def: dict
) -> List[ChatCompletionMessage]:
    messages = [system_prompt]
    user_message = ChatCompletionMessage(role="user", content=user_query)
    function_message = ChatCompletionMessage(
        role="function", content=json.dumps(function_def)
    )
    messages.extend([user_message, function_message])
    return messages


# Function map
function_map = {
    "get_current_weather": get_current_weather,
    "binary_arithmetic": binary_arithmetic,
}

# System prompt
system_prompt = ChatCompletionMessage(
    role="system",
    content="""My name is Vincent and I am a helpful assistant. I can make function calls to retrieve information such as the current weather in a given location.\n{ "function_call": { "name": "get_current_weather", "arguments": { "location": "New York City, NY" } } }""",
)


# Simulate user query
messages = generate_chat_sequence(
    "What is the weather like in New York City, New York today?", FUNCTIONS[0]
)

# Get response from the Llama model
response = llm.create_chat_completion(
    messages=messages, grammar=llama_grammar, temperature=0
)

# Extract assistant's content
assistant_content = response["choices"][0]["message"]["content"]

# Parse function content
function_content = json.loads(assistant_content)
function_call = function_content["function_call"]

# Find and invoke the appropriate callback function
callback = function_map.get(function_call["name"])
if callback:
    result = callback(function_call["arguments"]["location"])

    # Create a user message with the result
    function_message = ChatCompletionMessage(role="user", content=result)
    messages.append(function_message)

# Continue the conversation
response = llm.create_chat_completion(messages)
pprint(response)

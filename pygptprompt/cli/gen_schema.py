"""
pygptprompt/cli/gen_schema.py
"""
import ast
import json
from pathlib import Path

import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.introspection.schema import generate_function_schema
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


def extract_python_code(completion_response: dict) -> str:
    content = completion_response.get("content", "")
    start_idx = content.find("```python")
    end_idx = content.find("```", start_idx + 1)

    if start_idx == -1 or end_idx == -1:
        return ""

    return content[start_idx + 9 : end_idx].strip()


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
)
@click.option("--name", help="Function name")
@click.option("--params", help="Comma-separated list of parameters")
@click.option("--return_type", help="Return type of the function")
@click.option("--module_name", help="The name of the module for caching")
@click.option(
    "--gen_schema",
    type=bool,
    help="Generate a schema and save it to the configuration file.",
)
@click.option(
    "--provider",
    default="llama_cpp",
    help="Specify the model provider to use. Options are 'openai' for GPT models and 'llama_cpp' for Llama models.",
)
def main(
    config_path,
    name,
    params,
    return_type,
    module_name,
    gen_schema,
    provider,
):
    # Initialize system and user messages
    system = ChatModelResponse(
        role="system",
        content="Please generate a Python function based on the following description.",
    )
    user_prompt = f"Generate a Python function named {name} that takes parameters {params} and returns {return_type}."
    user = ChatModelResponse(role="user", content=user_prompt)
    messages = [system, user]

    # Initialize config and chat model
    config = ConfigurationManager(config_path)
    model_factory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    # Generate function description from model
    completion_response = chat_model.get_chat_completion(messages)
    print()  # NOTE: Add padding to stdout; Model output is flushed.

    # Render the function
    parsed_code = extract_python_code(completion_response)

    # Save the generated code to a file
    cache_path = Path(config.evaluate_path("app.cache"))
    module_path = cache_path / f"{module_name}.py"
    with open(module_path, "w") as f:
        f.write(parsed_code)

    # Parse the string to an AST
    parsed_ast = ast.parse(parsed_code)
    # Compile the AST into a code object
    code_obj = compile(parsed_ast, filename="<ast>", mode="exec")
    # Execute the code object in a given namespace (dictionary)
    namespace = {}
    exec(code_obj, namespace)
    # Extract the function from the namespace
    generated_code = namespace["add"]

    # Generate schema from the function
    schema = generate_function_schema(generated_code)

    if gen_schema:
        # Update function definitions in config
        functions = config.get_value("function.definitions", [])
        functions.append(schema)
        config.set_value("function.definitions", functions)
        config.backup()  # NOTE: Uses a timestamp to backup the file.
        config.save()  # CAUTION: This modifies the configuration file!
        print("Function schema updated.\n", json.dumps(schema))

    # Print summary
    print(f"Function generated and saved to {module_path}")


if __name__ == "__main__":
    main()

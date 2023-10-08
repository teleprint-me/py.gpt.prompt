"""
pygptprompt/introspection/schema.py

# Example usage with different functions or methods
a = A(5)  # bound property b is assigned the value of 5
schema_for_c = generate_function_schema(a.c)  # bound method
schema_for_d = generate_function_schema(A.d)  # static method

# Display the generated schemas
print(json.dumps(schema_for_c, indent=4))
print(json.dumps(schema_for_d, indent=4))
"""
import inspect
from typing import Any, Callable, Dict, List, Union


def set_class_info(schema: Dict[str, Any], func: Callable[..., Any]) -> None:
    if hasattr(func, "__self__"):
        schema["class"] = func.__self__.__class__.__name__


def set_function_info(schema: Dict[str, Any], func: Callable[..., Any]) -> None:
    if schema.get("class") is None:
        schema["name"] = func.__name__
    else:
        schema["name"] = f"{schema['class']}_{func.__name__}"


def set_description(schema: Dict[str, Any], func: Callable[..., Any]) -> None:
    doc = inspect.getdoc(func)
    if doc:
        doc_lines = doc.split("\n")
        schema["description"] = doc_lines[0]


def set_parameters(schema: Dict[str, Any], func: Callable[..., Any]) -> None:
    sig = inspect.signature(func)
    schema["parameters"] = {"type": "object", "properties": {}, "required": []}
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        param_info: Dict[str, Union[str, List[Any]]] = {"type": "any"}
        if param.annotation != inspect.Parameter.empty:
            param_info["type"] = param.annotation.__name__
        if param.default == inspect.Parameter.empty:
            schema["parameters"]["required"].append(name)
        else:
            param_info["enum"] = [param.default]
        schema["parameters"]["properties"][name] = param_info


def generate_function_schema(func: Callable[..., Any]) -> Dict[str, Any]:
    schema: Dict[str, Any] = {}
    set_class_info(schema, func)
    set_function_info(schema, func)
    set_description(schema, func)
    set_parameters(schema, func)
    return schema

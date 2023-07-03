# Prompting Guide

Welcome to the Prompting Guide! This document is designed to help you understand
and effectively utilize various styles of prompts when interacting with language
models.

## Zero-Shot Prompt

A zero-shot prompt allows you to request information or perform tasks without
providing explicit training examples. The model relies on its pre-existing
knowledge to generate responses.

**Example:**

Prompt: `"Generate a summary of the novel 'Pride and Prejudice.'"`

The model is expected to provide a concise summary of the novel without any
additional context or examples.

## One-Shot Prompt

A one-shot prompt involves providing a single specific training example or
demonstration to the model. The model uses this example to generalize its
understanding.

**Example:**

Prompt: `"In the following format, the capital of France is Paris."`

The model is expected to understand that the format is "The capital of [country]
is [capital]."

## Few-Shot Prompt

A few-shot prompt entails providing a small number of training examples to the
model. This approach helps the model learn from limited data and generalize its
understanding.

**Example:**

Prompt: `"Translate the following English words to Spanish: cat, dog, bird."`

The model is expected to provide the Spanish translations for each of the given
words.

## Priming Prompt

A priming prompt involves providing an initial context or partial sentence to
guide the model's response. This can help set the context and generate more
coherent outputs.

**Example:**

Prompt: `"Once upon a time, continue the fairy tale."`

The model is expected to generate a continuation of a fairy tale story starting
with "Once upon a time."

## Instructive Prompt

An instructive prompt includes explicit instructions or guidelines for the model
to follow. It helps control the behavior and output of the model.

**Example:**

Prompt:
`"Write a persuasive essay arguing for or against the use of genetically modified organisms (GMOs). Use at least three supporting reasons in your essay."`

The model is expected to generate a persuasive essay on the given topic,
including at least three supporting reasons.

## Conditional Prompt

A conditional prompt provides specific conditions or constraints to guide the
model's output. It can be in the form of input-output pairs, explicit criteria,
or instructions.

**Example:**

Prompt:
`"Translate the following English sentence to German: 'I love to travel.'"`

The model is expected to provide the German translation of the given English
sentence as specified in the prompt.

## API Function Prompt

API Function Prompting allows you to describe functions to the language model
and generate JSON objects adhering to the defined function schema. It enables
the model to perform specific actions or retrieve structured data.

**Example:**

Prompt:

```json
[
  {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
      },
      "required": ["location"]
    }
  }
]
```

**User:** What's the weather today for New York City, New York?

**Assistant:**

```python
get_current_weather(location="New York City, New York")
```

By incorporating both conditional prompting and function API calling, you can
effectively control the model's behavior and utilize its ability to generate
structured data or perform specific actions based on predefined conditions.

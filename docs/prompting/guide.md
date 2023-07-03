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

## Creative Prompt

A creative prompt encourages the model to generate imaginative or novel
responses. It often involves open-ended or ambiguous instructions.

**Example:**

Prompt: `"Create a short story about a mysterious key found in an old attic."`

The model is expected to generate a creative short story based on the given
prompt.

## Conditional Prompt

A conditional prompt provides specific conditions or constraints to guide the
model's output. It can be in the form of input-output pairs, explicit criteria,
or following an input, example, and output style.

**Example:**

Prompt:

```
Input: "Translate the following English sentence to German:"
Example: "I love to travel."
Output: "Ich liebe es zu reisen."
```

The model is expected to provide the German translation of the given English
sentence as specified in the input and output sections.

Feel free to experiment with these prompt styles and adapt them to your specific
needs. Remember, providing clear instructions and utilizing the appropriate
prompt style are key to achieving the desired results.

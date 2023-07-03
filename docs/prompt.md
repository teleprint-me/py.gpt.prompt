# Prompting Guide

Welcome to the Prompting Guide! This document will help you understand and
utilize various styles of prompts when interacting with language models.

## Zero-Shot Prompt

A zero-shot prompt allows you to request information or perform tasks without
providing explicit training examples. The model relies on its pre-existing
knowledge to generate responses. For example:

**Prompt:**

```
Generate a summary of the novel "Pride and Prejudice."
```

## One-Shot Prompt

A one-shot prompt involves providing a specific training example or
demonstration to the model. The model learns from this example to generalize its
understanding. For instance:

**Prompt:**

```
Input: The capital of France is
Output: Paris.
```

## Few-Shot Prompt

A few-shot prompt entails providing a small number of training examples to the
model. It helps the model learn from limited data and generalize its
understanding. For example:

**Prompt:**

```
Input: Translate the following words to Spanish: cat, dog, and bird.
Output: Gato, perro, y pájaro.
```

## Priming Prompt

A priming prompt involves providing an initial context or partial sentence to
guide the model's response. This can help set the context and generate more
coherent outputs. For instance:

**Prompt:**

```
Priming: Once upon a time,
Generate the next sentence of a fairy tale.
```

## Instructive Prompt

An instructive prompt includes explicit instructions or guidelines for the model
to follow. It helps control the behavior and output of the model. For example:

**Prompt:**

```
Write a persuasive essay arguing for or against the use of genetically modified organisms (GMOs). Use at least three supporting reasons in your essay.
```

## Creative Prompt

A creative prompt encourages the model to generate imaginative or novel
responses. It often involves open-ended or ambiguous instructions. For example:

**Prompt:**

```
Create a short story about a mysterious key found in an old attic.
```

## Conditional Prompt

A conditional prompt provides specific conditions or constraints to guide the
model's output. It can be in the form of input-output pairs or explicit
criteria. For instance:

**Prompt:**

```
Input: Translate the following English sentence to German.
English: "I love to travel."

Output: German translation of the input sentence.
```

Feel free to experiment with these prompt styles and adapt them to your specific
needs. Remember to provide clear instructions and utilize the desired prompt
style to achieve the desired results.

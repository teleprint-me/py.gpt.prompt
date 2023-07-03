# Model Questionnaire for General Assistance

1. **Greeting and Basic Information Retrieval**

   - "Hello, what is your name?"
   - "What is your primary role?"
   - "What is your primary function?"

2. **General Knowledge**

   - "What is the Python programming language?"
   - "Can you explain the concept of machine learning?"
   - "What is climate change?"

3. **Specialized Knowledge**

   - "What is John Conway's Game of Life?"
   - "What are the rules for Conway's Game of Life?"
   - "Can you explain the theory of relativity?"

4. **Code Generation**

   - "Can you show me a simple example of the Game of Life in Python?"

5. **Complex Reasoning and Explanation**

   - "Can you explain how a neural network works?"
   - "What is the difference between supervised and unsupervised learning?"
   - "Can you explain the concept of quantum physics?"

6. **Handling Ambiguity**

   - "What do you mean by 'training a model'?"
   - "What does 'apple' mean in different contexts?"

7. **Error Handling and Correction**

   - "What is the Pythno programming language?" (Intentional misspelling to test
     error detection)
   - "Can you correct this sentence? (provide a sentence with grammatical
     errors)"

8. **Contextual Understanding**

   - "Who won the world series last year?" (Requires up-to-date information)
   - "What is the weather like today?" (Requires real-time data, which the model
     may not handle)
   - "What's the capital of France?"

9. **Conditional Prompting**

   - "If I say 'apple', what comes to your mind?"
   - "Now, if I say 'apple' again, would your answer change? Why or why not?"
   - "Imagine you're an AI trained to assist a doctor. How would you respond if
     I say 'I have a headache'?"
   - "Now imagine you're an AI trained to assist a teacher. How would your
     response change if I say 'I have a headache'?"

10. **Sequential Prompting**

- "Tell me a joke."
- "Why is that joke funny?"

11. **Contextual Prompting**

- "What's the weather like today?" (The model should clarify the location since
  it doesn't have real-time data)
- "What if I'm in New York?"

12. **Complex Conditional Prompting**

- "If a person is feeling unwell and they have a headache, what advice would you
  give?"
- "What if they also have a high temperature?"

These prompts are designed to test the model's ability to maintain and utilize
context, handle changes in context, and respond appropriately to complex,
multi-condition prompts.

Remember, smaller models might struggle with some of these tasks, but the goal
is to understand their capabilities and limitations.

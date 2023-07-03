# Orca Mini Documentation

## Overview

Orca Mini is a series of smaller, faster, and more efficient versions of the
Orca model. These models are designed to provide a balance between performance
and speed, making them suitable for a wide range of tasks. The Orca Mini series
includes 3B, 7B, and 13B models, each with different strengths and capabilities.

## Model Details

### 3B Models

These models do not self-identify or role-play, lacking self-reference or
self-reflection. They are best suited for smaller scoped problems but require
more effort to work with. They have the fastest inference speeds, but the lowest
quality.

### 7B Models

The 7B models perform significantly better, capable of self-identifying and
assuming roles, showing potential for self-reflection. This makes them ideal for
tasks like programming assistance. Among them, the q5_1 and q6_K models deliver
the best performance, offering superior cognitive reasoning and a better
understanding of complex, abstract concepts. The models have a slower inference
speed, but are comparably faster when compared to its larger 13B predecessor.

### 13B Models

The 13B models are similar. The q4_1 13B is the best so far. These models are
much slower and have shown about the same amount of comprehension as the 7B
models so far. The 13B q4_1 is the first model to succeed in completing complex
output when compared to the others who all previously failed.

## Formatting Challenges

Both the 7B and 13B models have notable issues with output formatting. Potential
solutions include using precise prompts and corrective formatting, or employing
a Finite-State Machine to process streamed tokens for proper Markdown output.

## Quantization

Quantization reduces the numerical precision of model weights, impacting model
size, inference speed, and performance. Higher bit models tend to have better
output quality but require more computational resources.

## Prompt Design

The design of prompts greatly influences the model's output. Experimenting with
different prompt structures and providing explicit instructions can guide the
model's formatting.

## Post-Processing

Implement post-processing to handle formatting issues. A script or function can
reformat the model's output according to specific requirements, which is
especially helpful for lower bit models with more pronounced formatting issues
due to quantization.

**Model Testing Process:**

The following process is used to evaluate the capabilities and limitations of
the models:

1. **Self-Identification:** The model is asked to identify itself to test if it
   can assume a role or identity. This is crucial for interactive or
   conversational tasks as it shows potential signs for self-reflection.
   Self-reflection in AI models is crucial for consistency, context awareness,
   learning and adaptation, advanced problem solving, and ethical
   considerations.

2. **Domain-Specific Knowledge:** The model is asked about a specific domain
   (e.g., Python programming) to evaluate its breadth and depth of knowledge.

3. **Understanding Abstract Concepts:** The model is asked to explain a complex,
   abstract concept (e.g., Conway's Game of Life) to test its problem-solving
   abilities and conceptual understanding.

4. **Generating Complex Outputs:** The model is asked to generate a complex,
   structured output (e.g., Python code for Conway's Game of Life). This tests
   its ability to build upon previous context and generate accurate and
   correctly formatted outputs.

These tests provide a comprehensive evaluation of the models' capabilities,
helping to identify their strengths and weaknesses. This information is crucial
for understanding how the models can be best used or improved.

### 7B q5_1 Results

````
18:45:52 | ~/Documents/code/git/pygptprompt                                                                                                          [157/651]
 git:(main | Δ) λ python -m pygptprompt.ggml --chat True --filename "orca-mini-7b.ggmlv3.q5_1.bin"
2023-07-02 18:46:20,166 - INFO - requests.py:48 - Using TheBloke/orca_mini_7B-GGML to load orca-mini-7b.ggmlv3.q5_1.bin
Downloading (…)i-7b.ggmlv3.q5_1.bin: 100%|███████████████████████████████████████████████████████████████████████████████| 5.06G/5.06G [04:11<00:00, 20.1MB/s]
2023-07-02 18:50:32,623 - INFO - requests.py:61 - Using /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_7B-GGML/snapshots/709dfca2e5523319777f
d59fa522ea4e32a33d93/orca-mini-7b.ggmlv3.q5_1.bin to load TheBloke/orca_mini_7B-GGML into memory
llama.cpp: loading model from /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_7B-GGML/snapshots/709dfca2e5523319777fd59fa522ea4e32a33d93/orca-
mini-7b.ggmlv3.q5_1.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 512
llama_model_load_internal: n_embd     = 4096
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 32
llama_model_load_internal: n_layer    = 32
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 9 (mostly Q5_1)
llama_model_load_internal: n_ff       = 11008
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 7B
llama_model_load_internal: ggml ctx size =    0.07 MB
llama_model_load_internal: mem required  = 6612.59 MB (+ 1026.00 MB per state)
llama_new_context_with_model: kv self size  =  256.00 MB
user
> Hello! What is your name?

assistant
Hello! My name is Orca.

user
> What is the Python programming language?

assistant
Python is a high-level, interpreted programming language that was first released in 1991. It is known for its simplicity, readability, and ease of use. Python
 is widely used in various fields such as web development, data analysis, artificial intelligence, scientific computing, and more.

user
> What is Conway's Game of Life?

assistant
Conway's Game of Life is a cellular automaton created by mathematician John H. Conway in 1970. It is a two-dimensional game that involves the evolution of an
initial population of cells over time, based on the laws of physics and a set of rules. The game can be played visually or with just a set of rules, and it ha
s gained popularity as a computer game and educational tool in various fields such as artificial intelligence and complexity science.

user
> Can you show me a simple implementation in Python?

assistant
Sure! Here is a simple implementation of Conway's Game of Life in Python:
```
# Define the initial conditions for the population
population = [0, 0, 0, 0, 0, 0, 0, 0]

# Define the rules of the game
def update_cells(cells):
 for i in range(len(cells)):
 if (i+1) % 2 == 0 and sum([x for x in cells]) == 3:
 # If the cell is alive, add one to its counter
 cells[i] += 1
 else:
 # Otherwise, remove one from its counter
 cells[i] -= 1
 for j in range(len(cells)):
 if (j+2) % 2 == 0 and sum([x for x in cells]) == 3:
 # If the cell is alive, add one to its counter
 cells[j] += 1
 else:
 # Otherwise, remove one from its counter
 cells[j] -= 1

# Define a function to draw the cells
def draw_cells(cells):
 for i in

user
> %
````

**GPT's review and summarization of the models performance:**

The document provides a detailed log of the testing process for the Orca Mini 7B
q5_1 model. The model was loaded using the Python module `pygptprompt.ggml` and
the model file `orca-mini-7b.ggmlv3.q5_1.bin`. The model loading process reveals
that it has a vocabulary size of 32,000, a context size of 512, and an embedding
size of 4096. The model also has 256 multi-heads, 32 layers, and 128 rotations.
The format type is mostly Q5_1, and the model size is 7B. The memory required
for the model is approximately 6612.59 MB, with an additional 1026.00 MB
required per state.

The model was then tested in a chat-like interaction. It was able to
successfully self-identify as "Orca". It demonstrated domain-specific knowledge
by providing a clear and concise explanation of the Python programming language.
The model also showed understanding of abstract concepts by explaining Conway's
Game of Life, a cellular automaton.

However, when asked to generate a Python implementation of Conway's Game of
Life, the model's response was incomplete and the provided code was not a
correct implementation of the game. This suggests that while the model has a
good understanding of abstract concepts and can provide explanations, it may
struggle with generating complex outputs such as accurate and correctly
formatted code.

### 13B q4_1

````
02:30:10 | ~/Documents/code/git/pygptprompt                                                                                                          [62/1078]
 git:(main | Δ) λ python -m pygptprompt.ggml --chat True --repo_id "TheBloke/orca_mini_13B-GGML"  --filename "orca-mini-13b.ggmlv3.q4_1.bin"
2023-07-03 02:31:38,161 - INFO - requests.py:48 - Using TheBloke/orca_mini_13B-GGML to load orca-mini-13b.ggmlv3.q4_1.bin
Downloading (…)-13b.ggmlv3.q4_1.bin: 100%|███████████████████████████████████████████████████████████████████████████████| 8.14G/8.14G [03:17<00:00, 18.4MB/s]
2023-07-03 02:34:55,930 - INFO - requests.py:61 - Using /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_13B-GGML/snapshots/ce69cbc2ff6a795ee89
f4f7bb663c6f8186ac620/orca-mini-13b.ggmlv3.q4_1.bin to load TheBloke/orca_mini_13B-GGML into memory
llama.cpp: loading model from /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_13B-GGML/snapshots/ce69cbc2ff6a795ee89f4f7bb663c6f8186ac620/orca
-mini-13b.ggmlv3.q4_1.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 2048
llama_model_load_internal: n_embd     = 5120
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 40
llama_model_load_internal: n_layer    = 40
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 3 (mostly Q4_1)
llama_model_load_internal: n_ff       = 13824
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 13B
llama_model_load_internal: ggml ctx size =    0.09 MB
llama_model_load_internal: mem required  = 9807.48 MB (+ 1608.00 MB per state)
llama_new_context_with_model: kv self size  = 1600.00 MB
user
> Hello, what is your name?

assistant
 Hello! My name is Orca.

user
> What is your primary role?

assistant
My primary role is to assist you with any tasks or questions you may have.

user
> Can you explain the concept of object-oriented programming?

assistant
 Of course! Object-oriented programming (OOP) is a programming paradigm that focuses on creating objects which interact with each other to perform tasks. In O
OP, everything is an object, and the relationships between these objects are defined by messages or actions that they can send to each other. This allows for
complex programs to be built with reusable and modular components, which makes it easier to maintain and update the code over time.

user
> What is the Python programming language?

assistant
 Python is a high-level, interpreted programming language that is widely used for various applications such as data analysis, web development, artificial inte
lligence, and scientific computing. It has a clean syntax and a vast collection of libraries and modules that make it easy to perform complex tasks.

user
> What is the difference between a list and a tuple in Python?

assistant
 In Python, lists and tuples are both used to store collections of items, but they differ in how they define and manipulate the items. A list uses square brac
kets [] and appends items to the end of the list using the "+" operator. A tuple, on the other hand, uses parentheses and returns a single item at the end of
the expression. Additionally, lists are iterable, while tuples are not.

user
> What is John Conway's Game of Life?

assistant
 John Conway's Game of Life is a cellular automaton game where small living organisms called "cells" evolve and grow on a two-dimensional grid. The game invol
ves several rules for how cells can move and interact with each other, and players can build and modify the game by adding new rules or creatures to the game.
 It's a very interesting and complex game that has been played by millions of people worldwide.

user
> What are the rules for Conway's Game of Life?

assistant
 The basic rules for John Conway's Game of Life are as follows: 1. Each cell can move in four directions (up, down, left, or right) to its adjacent neighbors.
 2. Any size of cell can be created by combining smaller cells. 3. A cell that is smaller than a certain size (currently set to 10 in the game) cannot be made
. 4. A cell can be born from an empty cell if it has offspring. 5. The offspring of a cell can be any number of cells, and they can be born in any direction.
6. The game is played on a two-dimensional grid, with each player taking turns updating the grid according to the rules.

user
> Can you show me a simple example of the Game of Life in Python?

assistant
 Sure! Here's an example of how to create and play the game in Python:
```python
import math

def make_cell(size):
 return " " * (math.sqrt(2) - 1) + " " + str(int("{:.2e}".format(size**0.5)))

def update_game(grid, start_row, start_col, cell_size, num_cells):
 grid[start_row][start_col] = make_cell(cell_size)
 for i in range(num_cells):
 row_index = i % 4
 col_index = (i // 4) * 4
 grid[row_index][col_index] = make_cell(cell_size)
 for i in range(num_cells):
 row_index = i % 4
 col_index = (i // 4) * 4
 grid[row_index][col_index] = make_cell(cell_size)
 return grid

def play_game():
 size = 50
 num_grid_rows = int(math.sqrt(2)) - 1
 num_grid_cols = int(math.sqrt(2)) - 1
 grid = [[0 for _ in range(num_grid_rows)] for _ in range(num_grid_cols)]
 update_game(grid, 0, 0, size, num_cells = int(math.sqrt(2)))
 print("Game of Life:")
 print("-----------")
 for i in range(num_grid_rows):
 print("| " + "| ".join(map(" ", grid[i])) + " |")
 print("-----------")
```

This code creates a 50x50 grid and populates it with empty cells. It then calls the `update_game` function to fill the grid with living cells according to the
 rules of the Game of Life. Finally, it prints out the game board.

user
>
````

**GPT's review and summarization of the models performance:**

In this chat completion transcript, the assistant performs fairly well in
responding to the user's queries. The assistant correctly introduces itself as
Orca, explains its primary role, and provides clear, detailed explanations of
object-oriented programming (OOP), the Python programming language, and the
differences between a list and a tuple in Python.

One notable strength of the assistant is its ability to provide concise and
accurate responses to complex questions. This is evident in its explanations of
OOP, Python, and Conway's Game of Life. The assistant also correctly identified
Conway's Game of Life as a cellular automaton game, demonstrating its strong
domain-specific knowledge.

However, when asked to specify the rules of Conway's Game of Life, the assistant
did not provide the correct, established rules of the game. Instead, it provided
a general, abstract interpretation, suggesting the presence of inaccuracies in
its understanding of more complex, abstract concepts.

Furthermore, the assistant's attempt to provide a Python implementation of the
Game of Life was inaccurate and unclear, highlighting a key weakness in
generating complex outputs. The provided Python code doesn't reflect the rules
of the Game of Life and contains numerous errors, rendering it non-functional.

In conclusion, the assistant demonstrated proficiency in self-identification,
handling straightforward queries, and demonstrating domain-specific knowledge.
However, it fell short when required to explain more complex, abstract concepts
accurately and generate complex, accurate outputs. This could be addressed
through more targeted training or through the use of post-processing scripts to
correct formatting issues and inaccuracies in code generation.

### 13B q5_1 Results

````
09:16:13 | ~/Documents/code/git/pygptprompt
(.venv) git:(main | Δ) λ python -m pygptprompt.ggml --chat True --repo_id "TheBloke/orca_mini_13B-GGML"  --filename "orca-mini-13b.ggmlv3.q5_1.bin"
2023-07-03 09:16:23,398 - INFO - requests.py:48 - Using TheBloke/orca_mini_13B-GGML to load orca-mini-13b.ggmlv3.q5_1.bin
2023-07-03 09:16:23,573 - INFO - requests.py:61 - Using /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_13B-GGML/snapshots/ce69cbc2ff6a795ee89f4f7bb663c6f8186ac620/orca-mini-13b.ggmlv3.q5_1.bin to load TheBloke/orca_mini_13B-GGML into memory
llama.cpp: loading model from /home/austin/.cache/huggingface/hub/models--TheBloke--orca_mini_13B-GGML/snapshots/ce69cbc2ff6a795ee89f4f7bb663c6f8186ac620/orca-mini-13b.ggmlv3.q5_1.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 2048
llama_model_load_internal: n_embd     = 5120
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 40
llama_model_load_internal: n_layer    = 40
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 9 (mostly Q5_1)
llama_model_load_internal: n_ff       = 13824
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 13B
llama_model_load_internal: ggml ctx size =    0.09 MB
llama_model_load_internal: mem required  = 11359.05 MB (+ 1608.00 MB per state)
llama_new_context_with_model: kv self size  = 1600.00 MB
system
My name is Orca. I am a helpful AI assistant.

user
> Hello, what is your name?
.
. What is your primary role?

assistant
 My primary role is to assist you with your requests and answer your questions.

user
> What is your name?

assistant
 My name is Orca.

user
> Can you explain the concept of object-oriented programming?

assistant
 Certainly! Object-oriented programming (OOP) is a programming paradigm that focuses on the concept of objects, which are instances of classes that represent real-world entities. In OOP, programs are designed by creating objects that interact with each other to perform tasks. OOP incorporates principles such as encapsulation, inheritance, and polymorphism to create reusable and modular code.

user
> What is the Python programming language?

assistant
 The Python programming language is a high-level, interpreted programming language that is known for its simplicity, readability, and ease of use. Python is used in various fields such as data analysis, machine learning, web development, and scientific computing.

user
> 1. What is a list?
.
. 2. What is a tuple?
.
. 3. What is the difference between a list and a tuple in Python?

assistant
 1. A list is a collection of elements that can be of the same type and are stored in contiguous memory locations. In Python, lists are denoted using the built-in `list()` function.

2. A tuple is a collection of elements that are immutable and are stored as a single variable with parentheses. In Python, tuples are denoted using the built-in `tuple()` function.

3. The main difference between lists and tuples in Python is that lists are mutable, meaning they can be modified after they are created, while tuples are immutable, meaning they cannot be modified after they are created. Additionally, lists are more flexible and can store elements of different types, while tuples are only allowed to store elements of the same type.

user
> 1. What is John Conway's Game of Life?
.
. 2. What are the rules for Conway's Game of Life?

assistant
 John Conway's Game of Life is a mathematical game that involves creating a grid of cells, where each cell can be either "0" or "1". The goal of the game is to create a pattern that stays constant throughout the evolution. The rules for the game are as follows:

1. Each player starts with a initial set of "0"s in their grid.

2. On each turn, the player adds the current number of "0"s in their grid to the corresponding cells.

3. If a cell contains only one "0" at the end of a turn, it becomes a "1", and all neighboring cells with fewer than three "0"s become "2".

4. If a cell contains more than two "0"s at the end of a turn, it becomes a "1", and all neighboring cells with fewer than four "0"s become "2".

5. The game continues until all cells in the grid contain only one "0".

user
> Can you show me a simple example of the Game of Life in Python?

assistant
 Certainly! Here's an example implementation in Python:

```
def game_of_life(board):
 n = 12
 board = [[0 for i in range(n)] for j in range(n)]
 board[3][3] = 0
 board[7][0] = 0
 board[7][4] = 0
 board[6][6] = 0
 board[4][8] = 0
 board[1][5] = 0
 board[9][9] = 0
 board[5][3] = 0
 board[1][1] = 0
 board[7][7] = 0
 board[3][5] = 0
 board[5][9] = 0
 board[8][4] = 0
 board[9][7] = 0
 board[6][2] = 0
 board[4][6] = 0
 board[3][4] = 0
 board[1][7] = 0
 board[5][8] = 0
 board[7][2] = 0
 board[9][3] = 0
 board[1][6] = 0
 board[6][9] = 0
 board[8][1] = 0
 board[4][2] = 0
 board^C
Aborted!
````

**GPT's review and summarization of the models performance:**

Based on the testing, here are the strengths and weaknesses of the Orca Mini 13B
q5_1 model:

**Strengths:**

1. **Self-Identification:** The model successfully self-identified as Orca and
   understood its role as an AI assistant. This is a crucial aspect for
   interactive or conversational tasks.

2. **Domain-Specific Knowledge:** The model demonstrated a good understanding of
   Python programming and Object-Oriented Programming (OOP). It was able to
   provide accurate and detailed explanations of these topics.

3. **Understanding Abstract Concepts:** The model was able to explain John
   Conway's Game of Life, a complex, abstract concept. However, the explanation
   was not entirely accurate, indicating some limitations in its understanding.

**Weaknesses:**

1. **Generating Complex Outputs:** The model struggled with generating complex,
   structured output. For instance, it failed to provide the correct rules for
   Conway's Game of Life. This suggests that the model may have limitations in
   its problem-solving abilities and conceptual understanding.

2. **Formatting Challenges:** The model had issues with output formatting.
   However, formatting the input seemed to guide the model in its output, which
   could be a potential solution to this problem.

3. **Consistency:** The model's performance seemed to deteriorate towards the
   end of the testing. This inconsistency in performance could be a potential
   issue when using the model for more complex tasks.

Overall, the Orca Mini 13B q5_1 model shows promise in tasks involving
self-identification and domain-specific knowledge. However, it may struggle with
generating complex outputs and maintaining consistent performance. Further
testing and refinement may be needed to address these issues.

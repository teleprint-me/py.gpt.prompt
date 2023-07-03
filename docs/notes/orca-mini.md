# Orca Mini Notes and Observations

- **3B Models:** These models do not self-identify or role-play, lacking
  self-reference or self-reflection. They are best suited for smaller scoped
  problems but require more effort to work with. They have the fastest inference
  speeds, but the lowest quality.

- **7B Models:** The 7B models perform significantly better, capable of
  self-identifying and assuming roles, showing potential for self-reflection.
  This makes them ideal for tasks like programming assistance. Among them, the
  q5_1 and q6_K models deliver the best performance, offering superior cognitive
  reasoning and a better understanding of complex, abstract concepts. The models
  have a slower inference speed, but are comparably faster when compared to its
  larger 13B predecessor.

  - **Formatting Challenges:** The 7B models have notable issues with output
    formatting. Potential solutions include using precise prompts and corrective
    formatting, or employing a Finite-State Machine to process streamed tokens
    for proper Markdown output.

- **13B Models:** The 13B models are similar. The q4_1 13B is the best so far.
  These models are much slower and have shown about the same amount of
  comprehension as the 7B models so far. The 13B q4_1 is the first model to
  succeed in completing complex output when compared to the others who all
  previously failed.

  - **Formatting Challenges:** The 13B models also have issues with output
    formatting. The q4_1 model, for instance, failed to properly format the
    rules it listed. This is something to note and consider when using these
    models.

**GPT's Observations and Suggestions:**

- Models often rely on Markdown for formatting, but the formatting issues are
  tied to the model's interpretation and generation of Markdown output. By using
  specific prompts and precise formatting, the quality of generated Markdown can
  be improved.
- Implementing a Finite-State Machine to process the streamed tokens generated
  by the model can provide greater control over the output formatting.
- Quantization reduces the numerical precision of model weights, impacting model
  size, inference speed, and performance. Higher bit models tend to have better
  output quality but require more computational resources.
- Consider the specific task requirements when choosing a model. 7B models are
  suitable for self-identification and role-playing. 3B models can work for
  smaller problems with more prompt crafting. q5_1 or q6_K models offer superior
  cognitive reasoning despite slower inference.
- The design of prompts greatly influences the model's output. Experimenting
  with different prompt structures and providing explicit instructions can guide
  the model's formatting.
- Implement post-processing to handle formatting issues. A script or function
  can reformat the model's output according to specific requirements, which is
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

### q5_1 Results

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

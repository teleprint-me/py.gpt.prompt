# Model Specifications

- arxiv:2306.02707:
  [Orca: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/abs/2306.02707)

## Huggingface

- Creator: [Pankaj Mathur](https://huggingface.co/psmathur): Responsible for
  creating the models.
- Quantization: [Tom Jobbins](https://huggingface.co/TheBloke): Specialized in
  the quantization process for the models.

## Prompt Template

```
### System:
You are an AI assistant that follows instruction extremely well. Help as much as you can.

### User:
prompt

### Response:
```

or

```
### System:
You are an AI assistant that follows instruction extremely well. Help as much as you can.

### User:
prompt

### Input:
input

### Response:
```

## Compatibility

- Original llama.cpp quant methods: q4_0, q4_1, q5_0, q5_1, q8_0

  - These quantization methods have been quantized using an older version of
    llama.cpp to ensure compatibility with llama.cpp as of May 19th, commit
    2d5db48.
  - They are guaranteed to be compatible with any UIs, tools, and libraries
    released since late May.

- New k-quant methods: q2_K, q3_K_S, q3_K_M, q3_K_L, q4_K_S, q4_K_M, q5_K_S,
  q6_K
  - These new quantization methods are compatible with llama.cpp as of June 6th,
    commit 2d43387.
  - They are now also compatible with recent releases of text-generation-webui,
    KoboldCpp, llama-cpp-python, and ctransformers. For compatibility with other
    tools and libraries, please refer to their respective documentation.

## Explanation of the New k-quant Methods

The new methods available are:

- GGML_TYPE_Q2_K: "type-1" 2-bit quantization in super-blocks containing 16
  blocks, each block having 16 weights. Block scales and mins are quantized with
  4 bits. This effectively uses 2.5625 bits per weight (bpw).

- GGML_TYPE_Q3_K: "type-0" 3-bit quantization in super-blocks containing 16
  blocks, each block having 16 weights. Scales are quantized with 6 bits. This
  uses 3.4375 bpw.

- GGML_TYPE_Q4_K: "type-1" 4-bit quantization in super-blocks containing 8
  blocks, each block having 32 weights. Scales and mins are quantized with 6
  bits. This uses 4.5 bpw.

- GGML_TYPE_Q5_K: "type-1" 5-bit quantization. Same super-block structure as
  GGML_TYPE_Q4_K, resulting in 5.5 bpw.

- GGML_TYPE_Q6_K: "type-0" 6-bit quantization. Super-blocks with 16 blocks, each
  block having 16 weights. Scales are quantized with 8 bits. This uses 6.5625
  bpw.

- GGML_TYPE_Q8_K: "type-0" 8-bit quantization. Only used for quantizing
  intermediate results. The block size is 256. All 2-6 bit dot products are
  implemented for this quantization type.

Please refer to the Provided Files table below to see which files use which
methods and how.

## GGML Repository Identifiers

- Orca Mini 3B: TheBloke/orca_mini_3B-GGML
- Orca Mini 7B: TheBloke/orca_mini_7B-GGML
- Orca Mini 13B: TheBloke/orca_mini_13B-GGML

## Orca Mini 3B

| Name                         | Quant method | Bits | Size    | Max RAM required | Use case                                                                                                                                   |
| ---------------------------- | ------------ | ---- | ------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| orca-mini-3b.ggmlv3.q4_0.bin | q4_0         | 4    | 1.93 GB | 4.43 GB          | Original llama.cpp quant method, 4-bit.                                                                                                    |
| orca-mini-3b.ggmlv3.q4_1.bin | q4_1         | 4    | 2.14 GB | 4.64 GB          | Original llama.cpp quant method, 4-bit. Higher accuracy than q4_0 but quicker inference than q5 models.                                    |
| orca-mini-3b.ggmlv3.q5_0.bin | q5_0         | 5    | 2.36 GB | 4.86 GB          | Original llama.cpp quant method, 5-bit. Higher accuracy, higher resource usage, and slower inference.                                      |
| orca-mini-3b.ggmlv3.q5_1.bin | q5_1         | 5    | 2.57 GB | 5.07 GB          | Original llama.cpp quant method, 5-bit. Even higher accuracy, resource usage, and slower inference.                                        |
| orca-mini-3b.ggmlv3.q8_0.bin | q8_0         | 8    | 3.64 GB | 6.14 GB          | Original llama.cpp quant method, 8-bit. Almost indistinguishable from float16. High resource use and slow. Not recommended for most users. |

## Orca Mini 7B

| Name                           | Quant method | Bits | Size    | Max RAM required | Use case                                                                                                             |
| ------------------------------ | ------------ | ---- | ------- | ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| orca-mini-7b.ggmlv3.q2_K.bin   | q2_K         | 2    | 2.87 GB | 5.37 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for the attention.vw and feed_forward.w2 tensors, GGML_TYPE_Q2_K for others. |
| orca-mini-7b.ggmlv3.q3_K_L.bin | q3_K_L       | 3    | 3.60 GB | 6.10 GB          | New k-quant method. Uses GGML_TYPE_Q5_K for some tensors, else GGML_TYPE_Q3_K.                                       |
| orca-mini-7b.ggmlv3.q3_K_M.bin | q3_K_M       | 3    | 3.28 GB | 5.78 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for some tensors, else GGML_TYPE_Q3_K.                                       |
| orca-mini-7b.ggmlv3.q3_K_S.bin | q3_K_S       | 3    | 2.95 GB | 5.45 GB          | New k-quant method. Uses GGML_TYPE_Q3_K for all tensors.                                                             |
| orca-mini-7b.ggmlv3.q4_0.bin   | q4_0         | 4    | 3.79 GB | 6.29 GB          | Original llama.cpp quant method, 4-bit.                                                                              |
| orca-mini-7b.ggmlv3.q4_1.bin   | q4_1         | 4    | 4.21 GB | 6.71 GB          | Original llama.cpp quant method, 4-bit. Higher accuracy than q4_0 but quicker inference than q5 models.              |
| orca-mini-7b.ggmlv3.q4_K_M.bin | q4_K_M       | 4    | 4.08 GB | 6.58 GB          | New k-quant method. Uses GGML_TYPE_Q6_K for some tensors, else GGML_TYPE_Q4_K.                                       |
| orca-mini-7b.ggmlv3.q4_K_S.bin | q4_K_S       | 4    | 3.83 GB | 6.33 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for all tensors.                                                             |
| orca-mini-7b.ggmlv3.q5_0.bin   | q5_0         | 5    | 4.63 GB | 7.13 GB          | Original llama.cpp quant method, 5-bit. Higher accuracy, higher resource usage, and slower inference.                |
| orca-mini-7b.ggmlv3.q5_1.bin   | q5_1         | 5    | 5.06 GB | 7.56 GB          | Original llama.cpp quant method, 5-bit. Even higher accuracy, resource usage, and slower inference.                  |
| orca-mini-7b.ggmlv3.q5_K_M.bin | q5_K_M       | 5    | 4.78 GB | 7.28 GB          | New k-quant method. Uses GGML_TYPE_Q6_K for some tensors, else GGML_TYPE_Q5_K.                                       |
| orca-mini-7b.ggmlv3.q5_K_S.bin | q5_K_S       | 5    | 4.65 GB | 7.15 GB          | New k-quant method. Uses GGML_TYPE_Q5_K for all tensors.                                                             |
| orca-mini-7b.ggmlv3.q6_K.bin   | q6_K         | 6    | 5.53 GB | 8.03 GB          | New k-quant method. Uses GGML_TYPE_Q8_K for all tensors.                                                             |
| orca-mini-7b.ggmlv3.q8_0.bin   | q8_0         | 8    | 7.16 GB | 9.66 GB          | Original llama.cpp quant method, 8-bit. High resource use and slow. Not recommended for most users.                  |

## Orca Mini 13B

| Name                            | Quant method | Bits | Size     | Max RAM required | Use case                                                                                                                                   |
| ------------------------------- | ------------ | ---- | -------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| orca-mini-13b.ggmlv3.q2_K.bin   | q2_K         | 2    | 5.51 GB  | 8.01 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for the attention.vw and feed_forward.w2 tensors, GGML_TYPE_Q2_K for others.                       |
| orca-mini-13b.ggmlv3.q3_K_L.bin | q3_K_L       | 3    | 6.93 GB  | 9.43 GB          | New k-quant method. Uses GGML_TYPE_Q5_K for some tensors, else GGML_TYPE_Q3_K.                                                             |
| orca-mini-13b.ggmlv3.q3_K_M.bin | q3_K_M       | 3    | 6.31 GB  | 8.81 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for some tensors, else GGML_TYPE_Q3_K.                                                             |
| orca-mini-13b.ggmlv3.q3_K_S.bin | q3_K_S       | 3    | 5.66 GB  | 8.16 GB          | New k-quant method. Uses GGML_TYPE_Q3_K for all tensors.                                                                                   |
| orca-mini-13b.ggmlv3.q4_0.bin   | q4_0         | 4    | 7.32 GB  | 9.82 GB          | Original llama.cpp quant method, 4-bit.                                                                                                    |
| orca-mini-13b.ggmlv3.q4_1.bin   | q4_1         | 4    | 8.14 GB  | 10.64 GB         | Original llama.cpp quant method, 4-bit. Higher accuracy than q4_0 but quicker inference than q5 models.                                    |
| orca-mini-13b.ggmlv3.q4_K_M.bin | q4_K_M       | 4    | 7.87 GB  | 10.37 GB         | New k-quant method. Uses GGML_TYPE_Q6_K for some tensors, else GGML_TYPE_Q4_K.                                                             |
| orca-mini-13b.ggmlv3.q4_K_S.bin | q4_K_S       | 4    | 7.37 GB  | 9.87 GB          | New k-quant method. Uses GGML_TYPE_Q4_K for all tensors.                                                                                   |
| orca-mini-13b.ggmlv3.q5_0.bin   | q5_0         | 5    | 8.95 GB  | 11.45 GB         | Original llama.cpp quant method, 5-bit. Higher accuracy, higher resource usage, and slower inference.                                      |
| orca-mini-13b.ggmlv3.q5_1.bin   | q5_1         | 5    | 9.76 GB  | 12.26 GB         | Original llama.cpp quant method, 5-bit. Even higher accuracy, resource usage, and slower inference.                                        |
| orca-mini-13b.ggmlv3.q5_K_M.bin | q5_K_M       | 5    | 9.23 GB  | 11.73 GB         | New k-quant method. Uses GGML_TYPE_Q6_K for some tensors, else GGML_TYPE_Q5_K.                                                             |
| orca-mini-13b.ggmlv3.q5_K_S.bin | q5_K_S       | 5    | 8.97 GB  | 11.47 GB         | New k-quant method. Uses GGML_TYPE_Q5_K for all tensors.                                                                                   |
| orca-mini-13b.ggmlv3.q6_K.bin   | q6_K         | 6    | 10.68 GB | 13.18 GB         | New k-quant method. Uses GGML_TYPE_Q8_K for all tensors.                                                                                   |
| orca-mini-13b.ggmlv3.q8_0.bin   | q8_0         | 8    | 13.83 GB | 16.33 GB         | Original llama.cpp quant method, 8-bit. Almost indistinguishable from float16. High resource use and slow. Not recommended for most users. |

## Notes

- **3B Models:** These models do not self-identify or role-play. They are best
  suited for smaller scoped problems but require more effort to work with due to
  their lack of self-reference.

- **7B Models:** The 7B models perform significantly better, capable of
  self-identifying and assuming roles. This makes them ideal for tasks like
  programming assistance. Among them, the q5_1 and q6_K models deliver the best
  performance, offering superior cognitive reasoning and a better understanding
  of complex, abstract concepts.

  - **Formatting Challenges:** The 7B models have notable issues with output
    formatting. Potential solutions include using precise prompts and corrective
    formatting, or employing a Finite-State Machine to process streamed tokens
    for proper Markdown output.
  - Alternatively, streaming could be turned off, allowing for the output to be
    formatted before being displayed to the user. This simple approach, however,
    sacrifices the ability to stream token outputs.
  - Using streamed tokens with prompt-toolkit and pygments could recreate a
    ChatGPT UI-like experience. This would require careful planning and
    thoughtful implementation.
  - An extension of the previous idea could involve using prompt-toolkit to
    display the formatted output in a split window, either vertically or
    horizontally.

- **13B Models (To Be Evaluated):** The 13B models require further testing and
  evaluation.

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
   conversational tasks.

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

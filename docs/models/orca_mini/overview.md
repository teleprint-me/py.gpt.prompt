# Overview

Orca is a 13-billion parameter model developed to imitate the reasoning process
of large foundation models (LFMs). It learns from rich signals from GPT-4,
including explanation traces, step-by-step thought processes, and other complex
instructions, guided by teacher assistance from ChatGPT. The model is trained on
large-scale and diverse imitation data with judicious sampling and selection.

Orca surpasses conventional state-of-the-art instruction-tuned models such as
Vicuna-13B by more than 100% in complex zero-shot reasoning benchmarks like
Big-Bench Hard (BBH) and 42% on AGIEval. Moreover, Orca reaches parity with
ChatGPT on the BBH benchmark and shows competitive performance in professional
and academic examinations like the SAT, LSAT, GRE, and GMAT, both in zero-shot
settings without CoT; while trailing behind GPT-4.

The Orca models are implemented using [GGML](https://ggml.ai/), a tensor library
for machine learning designed to enable large models and high performance on
commodity hardware. GGML supports 16-bit float and integer quantization (e.g.,
4-bit, 5-bit, 8-bit), automatic differentiation, built-in optimization
algorithms (e.g., ADAM, L-BFGS), and is optimized for Apple Silicon. On x86
architectures, it utilizes AVX / AVX2 intrinsics. GGML also supports web
deployment via WebAssembly and WASM SIMD, has no third-party dependencies, and
allows zero memory allocations during runtime.

The Orca models are available in different quantized versions, including 3B, 7B,
and 13B models. Quantization reduces the numerical precision of the model's
weights, which can significantly reduce the model's size and increase its
inference speed. This makes the model more efficient and practical for
real-world applications, especially in resource-constrained environments.
However, quantization can also affect the model's performance and output
quality. Therefore, testing the quantized versions of these models is crucial to
understand the trade-off between model size, speed, and performance.

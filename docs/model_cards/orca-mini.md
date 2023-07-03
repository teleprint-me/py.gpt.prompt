# Model Specifications

- arxiv:2306.02707:
  [Orca: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/abs/2306.02707)

## Huggingface

- Pankaj Mathur: Creator: https://huggingface.co/psmathur
- Tom Jobbins: Quantization: https://huggingface.co/TheBloke

## Repositories

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

Certainly! Here's an updated version of your notes that incorporates my
observations and suggestions:

---

## Notes

- **3B models**: These models do not self-identify or role-play. They assume no
  identity or reference to self. They can be useful for smaller scoped problems,
  but require more time and effort to work with.

- **7B models**: The 7B billion models perform much better. They are willing to
  self-identify and assume a role, making them suitable for fulfilling the role
  of a programming assistant. The 4-bit and 5-bit models are the best performing
  ones. The 8-bit models have better cognitive reasoning but are slower during
  inference compared to the 4-bit and 5-bit models.

- **Formatting issues**: There are serious issues with the way the model formats
  its output. These issues may potentially be mitigated by using precise,
  accurate prompting and corrective formatting. One approach could be using a
  Finite-State Machine to process streamed tokens and produce properly formatted
  Markdown output.

- **TODO: 13B models**: Further testing and evaluation is needed for the 13B
  models.

**GPT's Observations and Suggestions**:

- Models tend to rely on Markdown for proper formatting, as it's a commonly used
  format for sharing information. However, the formatting issues you mentioned
  are related to the model's interpretation and generation of Markdown output.
  By providing specific and accurate prompts, as well as implementing a precise
  formatting process, we can improve the quality of the generated Markdown.

- It might be beneficial to set up a Finite-State Machine that can process the
  streamed tokens generated by the model and produce a Markdown format that
  meets your desired formatting requirements. This way, you can have more
  control over the output formatting and ensure it aligns with your
  expectations.

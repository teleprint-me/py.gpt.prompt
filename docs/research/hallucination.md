### Introduction

Hallucinations within AI models represent instances where the model's outputs
are not aligned with the input data. This documentation explores why these
hallucinations occur and the connection between various terms, such as
"perplexity," "imputation," and "stop-gap," in an attempt to elucidate potential
expressions, interpretations, and misunderstandings.

### Hallucinations and Perplexity

#### Hallucination

In AI, "hallucination" is when a model generates outputs not grounded in input
data. This may lead to erroneous output and is a complex issue to understand and
communicate.

#### Perplexity

Perplexity is a measure to evaluate how well a probability model predicts a
sample. In the context of hallucinations, it's an essential concept:

\[ \text{Perplexity}(x) = 2^{-\frac{1}{N}\sum\_{i=1}^{N} \log_2 p(x_i)} \]

A higher perplexity might indicate a greater likelihood of hallucinations, where
the model's predictions diverge from the true data distribution.

### Imputation

Imputation is the process of filling missing data, often used in AI. It can
sometimes lead to hallucinations due to misalignment of probability
distribution. This misalignment is a significant source of the erroneous output
in models.

### Stop-Gap: An Emergent Process

The term "stop-gap" is used to explain the phenomenon of attempting to
temporarily solve or mask the problem of hallucinations. It may be an emergent
process caused by imputation, where incorrect filling of data leads to
misalignment in the probability distribution.

### Conclusion

- "Hallucination" and "Perplexity" explain the phenomenon of unexpected outputs
  and how statistical evaluation can detect them.
- "Imputation" sheds light on a mechanism that may lead to hallucinations.
- "Stop-gap" encapsulates the temporary solutions or patches used to address
  these issues.

The exploration of these terms is a crucial step in improving the communication
about why and how AI models may produce erroneous outputs. By unraveling the
connections and implications of these terms, we've made strides towards a
clearer understanding of the complexities of AI models and their behavior,
particularly in relation to probability distribution.

**Genesis**

**Hypothesis**

Our journey began with an open-minded exploration, driven by curiosity rather
than a predefined goal. We sought to uncover connections between seemingly
unrelated domains, with the Law of Large Numbers guiding our initial steps.
Little did we anticipate that an accidental discovery would unveil an unexpected
bridge between financial concepts and machine learning principles.

During a playful exercise involving graphing the Principal Amount, a chance
observation struck us—what initially appeared as a financial trajectory bore an
uncanny resemblance to a loss function. This serendipitous moment led us to
realize the striking parallels between a growth model in finance and the
mechanics of machine learning training.

The accidental discovery became a catalyst for our investigation. We set out to
map these parallels and explore how concepts from the realm of compound interest
might offer insights into loss reduction and training dynamics in machine
learning. While our analogy isn't a direct translation of established
methodologies, it serves as an engaging thought experiment that bridges
mathematical frameworks across domains.

**Overview**

Initially, we employed the concept of compound interest from the realm of
finance, defined as follows:

```
target_amount = principal_amount * interval * growth_rate
```

- The `principal_amount` remains constant.
- The `growth_rate` is also consistent, as the periodic interest rate is fixed
  and the interval is 1 for daily compounding.
- The `interval` is the variable, representing the number of days.

Given the constancy of the principal amount and growth rate, the relationship
between the interval and target amount is linear. Clarifications aside, we can
now proceed with a proper review of our work, considering the accurate
interpretation of the frequency parameter.

**Terminology Conversion: Aligning Financial Model with Machine Learning**

1. **Periodic Rate (Financial) → Step Size (Machine Learning):**

   - Represents incremental change at each interval or step in the sequence.
     Reflects the magnitude of change during each update.

2. **Growth Rate (Financial) → Improvement Rate (Training) / Decay (Loss
   Function) (Machine Learning):**

   - Represents the rate of growth or decay over time. In training, it mirrors
     the model's learning rate. In a loss function, it signifies the reduction
     in loss over time.

3. **Target Amount (Financial) → Label/Desired Outcome (Machine Learning):**

   - Denotes the goal or desired result. In finance, it's the target financial
     amount. In machine learning, it's the correct label or outcome for a given
     input.

4. **Principal Amount (Financial) → Loss (Machine Learning):**

   - Serves as the starting point or baseline. In finance, it's the initial
     investment. In machine learning, it's the initial error or discrepancy
     between predicted and actual values.

5. **Interest Rate (Financial) → Learning Rate (Machine Learning):**
   - Reflects the rate of change over time. In finance, it's the percentage at
     which money grows or decays. In machine learning, it governs the rate at
     which the model's weights update during training.

Through these parallels, we establish an analogy between a financial model
(compound interest) and a machine learning context (training and loss
reduction). This imaginative mapping unveils shared patterns and structures
bridging these two domains.

Notably, this analogy is conceptual and exploratory. It exposes intriguing
connections, although it might not directly correlate with established
mathematical or machine learning techniques.

**Expression**

By linking the label (target amount) with loss, epoch, learning rate, and
frequency, we can express the relationship as follows:

```
label = loss * epoch * improvement_rate
label = loss * epoch * (1 + learning_rate / frequency)^epoch
```

Here, the label signifies the desired outcome or target value. This equation
showcases how loss, learning rate, and epoch interact to approach the target.

While a creative analogy, this may not directly correspond to a specific machine
learning algorithm or loss function.

**Expressing Loss**

**Step Size:** Represents change magnitude during each training update, akin to
the periodic interest rate in finance.

```
step_size = 1 + learning_rate / frequency
```

**Improvement Rate (Growth Rate):** Indicates the rate of loss reduction during
training, resembling the growth rate in finance.

```
improvement_rate = step_size^epoch
improvement_rate = (1 + learning_rate / frequency)^epoch
```

**Loss (Principal Amount):** The loss function embodies prediction error, akin
to the principal amount in compound interest.

```
loss = desired_loss / (epoch * improvement_rate)
loss = desired_loss / (epoch * (1 + learning_rate / frequency)^epoch)
```

**Target Amount (Label/Desired Outcome):** Mirrors accumulated value per step,
resembling desired outcome or label in machine learning.

```
target_amount = principal_amount * epoch * improvement_rate
target_amount = principal_amount * epoch * (1 + learning_rate / frequency)^epoch
```

Through these parallels, we creatively explored connections between a financial
growth model (compound interest) and a hypothetical machine learning training
scenario. While not directly applicable to a standard machine learning
algorithm, it sheds light on shared mathematical structures and patterns across
domains.

**Calculate the Label**

We adapted the concept of compound interest for a hypothetical machine learning
scenario:

- `Step Size (S)`: Represents change magnitude per step, linked to learning rate
  and frequency.
- `Improvement Rate (I)`: Growth/improvement rate per step, calculated as step
  size raised to epoch.
- `Label/Desired Outcome (A)`: Target value, represented as loss _ epoch _
  improvement rate.

Equation: `A = L * E * (1 + R / F)^E`

**Calculate the Loss**

We investigated the inverse relationship, focusing on loss calculation:

- `Loss (L)`: Error between predicted and actual values, akin to principal
  amount.
- `Epoch (E)`: Complete pass through training data, like interval in compound
  interest.
- `Desired Loss (D)`: Minimum loss sought, akin to target amount.

Equation: `L = D / (E * (1 + R / F)^E)`

**Conclusion**

This imaginative analogy draws parallels between compound interest mathematics,
statistical convergence, and hypothetical loss functions in machine learning.
Although not a direct fit for real-world scenarios, it has been an engaging and
thought-provoking endeavor.

Our findings underscore the universal nature of mathematical concepts across
disciplines, highlighting the potential for innovative insights through creative
exploration.

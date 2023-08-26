# The Genesis Model: Exploring How Financial Models might apply to Generative AI

## Abstract

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

## Introduction

In the vast landscape of mathematical modeling, two seemingly disparate fields
often operate in isolation: finance and machine learning. At a glance, these
disciplines may appear to have little in common. Finance typically deals with
the management of money, investments, and risk, while machine learning explores
algorithms and statistical models to enable computers to perform tasks without
explicit programming. However, a closer examination reveals intriguing parallels
that beckon further exploration.

This document embarks on an interdisciplinary journey to uncover the underlying
connections between financial models and machine learning algorithms. A
particular point of intrigue lies in the relationship between Empirical Risk
Minimization (ERM), a principle fundamental to machine learning, and the Value
Averaging strategy commonly employed in finance.

ERM, an NP-hard problem, involves the search for a model that minimizes the
average loss on a given dataset. In contrast, the Value Averaging strategy
introduces a form of linearity within financial planning, a characteristic that
may at first seem unrelated to ERM. However, the correlation between these
concepts forms a bridge that connects the complexities of machine learning with
the principles of financial management.

The analogy, while compelling on a conceptual level, is admittedly rough and
sparse in its current form. The correlation is primarily based on scalar values,
and it's in the early stages of development, meaning nothing concrete is
directly applicable at this moment.

The inspiration for this exploration was sparked by the visual representation of
the Principal Amount over time, resembling a loss (or risk) function commonly
encountered in machine learning. Though the analogy may have limitations – for
instance, machine learning models often work with matrices, contrasting the
scalar approach in finance – the potential insights derived from bridging these
domains warrant a detailed investigation.

This document aims to:

- Elucidate the conceptual connections between finance and machine learning.
- Recognize the constraints and limitations that might hinder direct
  applicability.
- Lay the groundwork for potential innovations, with the understanding that the
  work is exploratory in nature and may lead to novel intersections between
  these fields.

While the connections might not yet be fully realized, this exploration marks
the beginning of a promising pathway, one that could yield profound insights
into both fields and create opportunities for unprecedented collaboration.

## Background and Conceptual Framework

### Mathematical Concepts in Finance and Machine Learning

In the field of finance, concepts like compound interest are central to
understanding how money grows over time. The equation for calculating the target
amount with daily compounding can be expressed as:

```plaintext
periodic_interest_rate = interest_rate / frequency
growth_rate = pow(periodic_interest_rate, interval)
target_amount = principal_amount * interval * growth_rate
```

In machine learning, similar principles apply but within the context of model
training and loss reduction. The common goal is optimization, whether that's
maximizing financial gain or minimizing predictive errors.

### Exploring the Analogy: Graphing the Principal Amount Over Time

The code snippet below illustrates the relationship between the principal amount
and the number of days, aiming to shed light on how this financial concept
translates into a machine learning context:

```python
# Importing the Matplotlib library for plotting
import matplotlib.pyplot as plt


# Redefining the functions and constants, and running the code block for graphing
def calculate_periodic_interest_rate(interest_rate, frequency):
    return 1 + (interest_rate / frequency)


def calculate_principal_amount(
    target_amount, interval, periodic_interest_rate
):
    return target_amount / (interval * pow(periodic_interest_rate, interval))


# Constants for the simulation
daily_interest_rate = 5 / 100  # 5% daily interest rate
frequency = 365  # daily compounding
interval_range = 30  # 30 days
target_amount_goal = 3_000_000  # Target Amount of 3,000,000 Satoshi's

# Lists to store the results for graphing
principal_days = []
principal_satoshis = []

# Calculate the periodic interest rate
periodic_rate = calculate_periodic_interest_rate(
    daily_interest_rate, frequency
)

# Calculate the principal amount needed to reach the target amount for each interval in the range
for interval in range(1, interval_range + 1):
    principal_amount = calculate_principal_amount(
        target_amount_goal, interval, periodic_rate
    )

    principal_days.append(interval)
    principal_satoshis.append(principal_amount)

# Displaying the results in a graph
plt.plot(principal_days, principal_satoshis, marker="o", color="blue")
plt.title("Principal Amount Needed to Reach 3,000,000 Sats (Daily Trading)")
plt.xlabel("Days")
plt.ylabel("Principal Amount (Sats)")
plt.grid(True)
plt.show()
```

While the graph might initially suggest a linear relationship between the
interval and the target amount, it's crucial to clarify that this observation is
a simplification. The equation for calculating the target amount implies a more
complex, exponential relationship due to the power term
(`pow(periodic_interest_rate, interval)`).

This simplified interpretation arises from dealing exclusively with scalar
values. We have deliberately avoided the complexities of vector spaces and
sequence modeling inherent in advanced machine learning techniques at this stage
of the discussion.

Given that the frequency parameter plays a role in both financial modeling and
potentially in machine learning—perhaps as a hyperparameter dictating how often
a model is updated—elaborating on its role and significance would be beneficial
in the final document.

### Aligning Financial Models with Machine Learning Terminologies

We align the financial model of compound interest with machine learning context,
elucidating shared patterns and structures through the following terminology
conversion:

- The `principal_amount` remains constant.
- The `interval` is the variable, representing the number of days.
- The `growth_rate` is exponential, as the `periodic_interest_rate` is fixed and
  the `interval` is utilized for regular compounding.

However, it's essential to note that while these relationships appear
straightforward, the exponential nature of compound interest suggests a more
complex relationship.

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

### Constraints and Limitations

This analogy is conceptual and serves as a foundational framework. It
deliberately employs scalar values to represent financial and machine learning
concepts, avoiding the complexities of vector spaces and sequence modeling
inherent in advanced machine learning techniques. These limitations need to be
acknowledged, particularly if one aims to extend these insights into practical
applications.

## Experimental Quantitative Analysis

By linking the label (target amount) with loss, epoch, learning rate, and
frequency, we can express the relationship as follows:

```
label = loss * epoch * improvement_rate
label = loss * epoch * (1 + learning_rate / frequency)^epoch
```

Here, the label signifies the desired outcome or target value. This equation
showcases how loss, learning rate, and epoch interact to approach the target.

While this serves as a creative analogy for understanding complex interactions
in machine learning, it's crucial to note that the equation may not directly
correspond to any specific machine learning algorithm or loss function. Exercise
caution if attempting to apply this concept directly.

### Expressing Loss

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
label = loss * epoch * improvement_rate
label = loss * epoch * (1 + learning_rate / frequency)^epoch
```

Through these parallels, we creatively explored connections between a financial
growth model (compound interest) and a hypothetical machine learning training
scenario. While not directly applicable to a standard machine learning
algorithm, it sheds light on shared mathematical structures and patterns across
domains.

### Example: A Hypothetical Case Study

To elucidate, consider a simple example where `loss = 0.5`, `epoch = 10`,
`learning_rate = 0.1`, and `frequency = 100`. Using the equations:

- Improvement Rate: `(1 + 0.1 / 100)^10`
- Label: `0.5 * 10 * (1 + 0.1 / 100)^10`

The results can offer practical insights into how these variables interact.

### Calculate the Label

We adapted the concept of compound interest for a hypothetical machine learning
scenario:

- `Step Size (S)`: Represents the magnitude of change at each step, related to
  the learning rate and frequency.
- `Improvement Rate (I)`: The growth or improvement rate at each step,
  calculated as the step size raised to the epoch.
- `Label or Desired Outcome (A)`: The accumulated value or target, represented
  as the loss times the epoch times the improvement rate.

Equation: `A = L * E * (1 + R / F)^E`

### Calculate the Loss

We investigated the inverse relationship, focusing on loss calculation:

- `Loss (L)`: The error between predicted and actual values, analogous to the
  principal amount in finance.
- `Epoch (E)`: A full pass through the training data, analogous to the interval
  in compound interest.
- `Desired Loss (D)`: The minimum loss we aim to achieve, analogous to the
  target amount.
- **Note**: `D` is equivalent to `A` from the `Label` calculation which was
  originally defined as the `Desired Outcome`.

Equation: `L = D / (E * (1 + R / F)^E)`

### Exploring the Analogy: Graphing the Target Amount Over Time

In this section, we graphically represent how the target amount changes with
respect to different parameters. This offers a visual insight into the
relationship between loss, epochs, learning rate, and frequency.

```py
# Importing the Matplotlib library for plotting
import matplotlib.pyplot as plt


# Redefining the functions and running the same code block for graphing
def calculate_periodic_interest_rate(interest_rate, frequency):
    return 1 + (interest_rate / frequency)


def calculate_growth_rate(periodic_interest_rate, interval):
    return pow(periodic_interest_rate, interval)


def calculate_target_amount(principal_amount, interval, growth_rate):
    return principal_amount * interval * growth_rate


# Constants for the simulation
daily_principal_amount = 50_000  # 50,000 Sats
daily_interest_rate = 5 / 100  # 5% daily interest rate
frequency = 365  # daily compounding
interval_range = 30  # 30 days

# Lists to store the results for graphing
refactored_days = []
refactored_satoshis = []

# Starting with the initial trading amount as the principal
current_principal = daily_principal_amount

# Calculate the periodic interest rate
periodic_rate = calculate_periodic_interest_rate(
    daily_interest_rate, frequency
)

# Calculate the potential growth of Satoshis for each day in the interval range
for interval in range(1, interval_range + 1):
    # Calculating the growth rate
    growth_rate = calculate_growth_rate(periodic_rate, 1)

    # Calculating the target amount
    target_amount = calculate_target_amount(current_principal, 1, growth_rate)

    refactored_days.append(interval)
    refactored_satoshis.append(target_amount)

    # Using the target amount as the new principal for the next day's calculation
    current_principal = target_amount

# Displaying the results in a graph
plt.plot(refactored_days, refactored_satoshis, marker="o", color="purple")
plt.title(
    "Refactored Potential Growth of 50,000 Sats with Compounding (Daily Trading)"
)
plt.xlabel("Days")
plt.ylabel("Satoshis (Sats)")
plt.grid(True)
plt.show()
```

By updating the `current_principal` to `target_amount` at the end of each loop
iteration, we're essentially rolling over the calculated target amount to serve
as the new "principal amount" for the next day's calculation. This is what makes
it "compound" rather than just "simple" growth. In other words, we're not just
accumulating based on the original principal amount but also on the gains made
from prior periods.

Removing this line would make each day's target amount only based on the
original `daily_principal_amount`, effectively turning it into simple interest,
where the growth is linear with respect to time.

In a machine learning context, the exponential curve could represent a model
that rapidly improves its performance, possibly indicating that it's learning
effectively. On the other hand, the straight line (or absence of an exponential
curve) might represent a model that is learning, but not at an accelerating
rate, possibly indicating a need for tuning hyperparameters, modifying the
architecture, or exploring other strategies for improvement.

**Note:**

1. The graph aims to show the progression of the target amount over time,
   allowing for better understanding of how each parameter affects the learning
   process.
2. Different configurations of learning rate and frequency will yield different
   curve shapes, highlighting the sensitivity of the model to these parameters.
3. While insightful, the graph may have limitations in capturing real-world
   complexities. Caution should be exercised when extrapolating these results to
   actual machine learning algorithms.

### Potential Applications for Compounded Learning

It's intriguing to consider the idea of a compounding learning rate in machine
learning scenarios. Typically, learning rates are treated as fixed
hyperparameters or adapted through techniques like learning rate annealing,
which usually involves decreasing the learning rate over time. However, the
concept of a compounding learning rate could introduce an entirely new dimension
to model training.

In financial terms, compound interest works wonders because it's the "interest
on interest" that starts to accumulate. If you translate this concept to machine
learning, a compounding learning rate could, in theory, allow the model to learn
"faster on what it has already learned faster," assuming it's moving in the
right direction. This kind of "exponential learning" might allow the model to
rapidly converge to an optimal or near-optimal solution.

That said, introducing a compounding learning rate could also introduce risks,
such as the potential for the model to overshoot the optimal point and diverge.
However, if well-tuned, it might offer a way to accelerate learning in the
initial stages and then stabilize as it nears an optimal solution, much like how
some investment strategies aim to maximize returns early on and then transition
to a more conservative stance as the goal nears.

### Further Work

For those interested in extending this framework, some potential directions
include:

- Experimenting with vector spaces to explore how this analogy holds in
  multi-dimensional scenarios.
- Conducting empirical studies that apply these concepts to real-world financial
  and machine learning models.

## The Loss Function Analogy

1. **Market Price**: Comparable to an input or parameter value in machine
   learning used for predictions. In the context of the Value Averaging
   strategy, it denotes the buying or selling price.

2. **Target Value (Label)**: In machine learning, it's the actual outcome we aim
   to predict. In the Value Averaging strategy, it signifies the desired
   investment value at each interval (Current Target).

3. **Current Value (Prediction)**: In Value Averaging, this is the actual
   investment value at a given time. In machine learning, it corresponds to the
   model's prediction based on input features (Market Price).

4. **Trade Amount (Loss)**: This draws a parallel to the loss function. In Value
   Averaging, the Trade Amount represents the difference between the Current
   Target (Label) and the Current Value (Prediction). In machine learning, this
   difference mirrors the loss, indicating the deviation between prediction and
   actual target.

Now, let's explore this concept mathematically:

### Mathematical Representation

In Value Averaging:

```
Trade Amount = Current Target - Current Value
```

In Machine Learning (Loss Function):

```
Loss = Target Value (Label) - Prediction
```

### Equivalent Analogy

- Trade Amount ↔ Loss
- Current Target ↔ Target Value (Label)
- Current Value ↔ Prediction
- Market Price ↔ Input Features

The resemblance between these concepts is intriguing, offering a fresh
perspective on the relationships that can be drawn between financial modeling
and machine learning. A thoughtful approach, beginning with the exploration of
Mean Squared Error (MSE), leads to a deeper understanding. Let's now explore the
integration of the components of our analogy with the concept of MSE.

### Definitions:

- `A`: Target value, representing the desired future investment value.
- `L`: Trade amount or Loss, denoting the difference between target and current
  value.
- `D`: Desired value for each interval (constant or variable).
- `E`: Number of intervals.
- `R`: Rate of return.
- `F`: Frequency of compounding.

### Formulating the Analogy with MSE

In machine learning, MSE calculates the average of squared differences between
predicted and actual target values. Mathematically:

```
MSE = (1/n) * n_Σ_i=1 (Prediction_i - Target_i)^2
```

In our analogy, MSE signifies the average of squared differences between
investment's current value and desired target value over intervals:

```
MSE = (1/E) * E_Σ_i=1 (Current Value_i - A_i)^2
```

Where:

- `Current Value_i`: Investment's actual value at interval `i`.
- `A_i`: Target value at interval `i`, calculated as
  `A_i = L * E * (1 + R / F)^i`.

### Application

MSE in this context provides insight into alignment of investment strategy with
targets. Lower MSE suggests close alignment, while higher MSE indicates
deviations.

### Further Exploration

We can simulate various investment scenarios, calculating MSE to assess
strategy's alignment with targets. Exploring how parameters like return rate or
compounding frequency influence MSE offers an intriguing avenue.

### Financial Modeling - Value Averaging Strategy

#### Variables

- `A`: Target Value (Desired Value)
- `D`: Current Value (Actualized Value)
- `L`: Trade Amount
- `E`: Interval
- `R`: Growth Rate
- `F`: Frequency

#### Equations

- Target Value: `A = E * (1 + R / F)^E`
- Trade Amount: `L = A - D`

### Machine Learning - Loss Function Analogy

#### Variables

- Market Price: Corresponds to input/parameter value in the initial layer
- Target Value (Label): `A`
- Prediction (Current Value): `D`
- Trade Amount (Loss): `L`

#### Analogy Summary

- The Market Price can be thought of as the input to a machine learning model.
- The Target Value corresponds to the actual label or desired outcome.
- The Current Value is akin to the prediction made by the model.
- The Trade Amount serves as the "loss," representing the difference between the
  Target and Current Values.

### Cross-Domain Parallels

1. **Target Value (Desired Value)**: In both domains, this represents the
   "ideal" or "goal" outcome.
2. **Current Value (Actualized Value)**: Represents the "current state" in both
   domains.
3. **Trade Amount**: Serves as the "error" or "deviation" from the desired
   outcome. Similar to the loss in machine learning.
4. **Interval (E)**: Time steps in financial modeling, could be analogous to
   epochs or batches in machine learning.
5. **Growth Rate (R)**: In finance, this is the expected growth rate. In ML, it
   could be seen as the learning rate.

## Reward Function for Investment Decision-Making

In the context of investment decision-making, we aim to create a reward function
that guides the choice between buying and selling based on various factors such
as current balance, target amount, and market performance. This reward function
leverages the concepts of normalization, impact functions, and weighted
aggregation to provide a comprehensive assessment of the investment decision.

### Variables

1. **Current Balance (B):** The current amount of funds available for
   investment.
2. **Target Amount (T):** The desired amount for investment.
3. **Market Performance (P):** Indicators of the market's performance.

### Steps

1. **Normalize Variables:**

   - Normalize each variable to a common scale to ensure comparability.

2. **Assign Weights:**

   - Assign weights (Wb, Wt, Wp) to each normalized variable to indicate their
     relative importance.

3. **Impact Functions:**

   - Define impact functions for each normalized variable:
     - Impact of balance (Ib) = B (normalized value)
     - Impact of target (It) = T (normalized value)
     - Impact of market performance (Ip) = P (normalized value)

4. **Combined Impact Score:**

   - Calculate the combined impact score by taking the dot product of normalized
     variables and their respective weights:
     - Combined Impact Score = (Wb \* Ib) + (Wt \* It) + (Wp \* Ip)

5. **Normalization Factor:**

   - Choose a normalization factor based on the desired range of reward values.

6. **Normalized Reward Value:**

   - Divide the combined impact score by the normalization factor to obtain the
     normalized reward value.

7. **Scale to Desired Range:**
   - Scale the normalized reward value to fit within the desired range:
     - Scaled Reward = Normalized Reward Value \* (Upper Range - Lower Range) +
       Lower Range

### Iteration and Refinement

- Experiment with different normalization factors, weights, and impact functions
  to fine-tune the reward function.
- Validate the reward function's effectiveness using historical data or
  simulations.
- Iterate and adjust the approach based on observed outcomes and real-world
  investment strategies.

The reward function developed through this approach offers a structured way to
guide investment decisions by considering multiple variables and their impacts.
By leveraging normalization, impact functions, and weighted aggregation, this
reward function aims to provide insights that align with investment goals and
market dynamics.

## Limitations and Pitfalls of Applicability

There are some highly nuanced points that really highlight the limitations of
purely mathematical or algorithmic approaches to trading and finance. The nature
of trading is much more volatile and subject to various non-mathematical
factors, like market sentiment and human psychology, that aren't easily captured
in equations or loss functions.

### Pitfalls of the "Greedy Function"

Maximizing the reward function could result in creating a "Greedy Function". The
"greedy function" approach, while theoretically sound, doesn't account for these
subtleties. It's a bit like trying to use a hammer where a scalpel is required.
What might be a loss function in one context (ML) becomes a convoluted
combination of both reward and loss in another (trading).

### Dangers of Over-simplification

This underlines the danger of over-simplification, especially in something as
complex and multi-faceted as trading. In machine learning, the loss function
guides the model toward a more accurate representation of reality. In trading,
however, reality itself is far too complex to be captured by a single metric.
Different strategies like Value Averaging may work in some contexts but fail
catastrophically in others, as you pointed out with the example of the housing
crisis.

### Context Matters

Different asset types, such as commodities, like Gold or Bitcoin, should be
considered. What works for one asset class may be disastrous for another. For
example, a strategy focused on short-term gains might work well in a volatile
market but fail to capture the long-term value of more stable assets.

### The Human Element

The emotional and psychological aspects of trading are yet another layer that's
difficult to quantify. While machine learning models may strive to be more
"rational," human traders have gut instincts, fears, and aspirations that can
drive the market in unpredictable ways.

So, while it was a fruitful exercise to explore the mathematical analogies and
theoretical frameworks, it's paramount in observing that the application to
trading is far from straightforward. However, these considerations can offer
valuable insights that might inform more nuanced trading algorithms or
risk-assessment tools that take these complexities into account.

## Potential ML Translations from Financial Models:

1. **Adapting Variables**: Adapting financial terms to machine learning can be
   an abstract but intriguing task. For example, "Current Balance" could be
   viewed as the "current state" of the machine learning model, including its
   accuracy, precision, and other performance metrics. "Target Amount" could be
   translated into a desired accuracy or minimal loss.

2. **Trade Amount as Optimization Target**: This is an exciting idea. In
   reinforcement learning, the trade amount can be very analogous to the reward
   gained from an action, serving as an optimization target. Similarly, in
   supervised learning, it might be used as a part of a custom loss function
   aiming to maximize this "trade amount" in a prediction task.

3. **Compounding Interest and Exponential Growth**: The formula
   `A = L * E * (1 + R / F)^E` has an exponential term, which naturally leads to
   the idea of exponential growth. In machine learning, particularly in
   long-term sequence predictions or time series analysis, exponential growth
   factors can be crucial. This formula might be used to better model such data,
   or even as a custom loss function designed for those specific types of data.

The equations for Label and Loss calculation can be considered as custom loss
functions that model the task's complexity and change over epochs.

## Conclusion

This imaginative analogy draws parallels between compound interest mathematics,
statistical convergence, and hypothetical loss functions in machine learning.
Although not a direct fit for real-world scenarios, it has been an engaging and
thought-provoking endeavor.

Our findings underscore the universal nature of mathematical concepts across
disciplines, highlighting the potential for innovative insights through creative
exploration.

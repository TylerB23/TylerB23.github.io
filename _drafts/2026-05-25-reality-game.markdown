---
layout: post
categories: Technical
title: "Recreating the Reality Game"
excerpt: "Expanding on an interesting mathematical finance paper."
toc: true
---

# Introduction #

In this post, I recreate a model of an evolutionary game put forward by
mathematical finance researchers in 2009. Their work suggests that, in systems
where participants interact with one another to affect the probability of future
outcomes, it can take a long time for steady state behavior to emerge. This has
interesting implications for financial markets (for example, the interaction
between hedge fund strategies resulting in inefficencies that persist for
significant periods of time). In the second half of the post, I extend their
model slightly to see if the qualitative behavior persists.

First, some background on how I found the paper and why I found it so
compelling.

## Background ##

I've been working my way through a recommended reading list for those interested
in quantitative trading by Kris Abdelmessih, a former options trader at SIG who
writes the Moontower substack. So far I've read Howard Marks' *The Most
Important Thing*, Agustin Lebron's *The Laws of Trading*, and Annie Duke's
*Thinking in Bets*. I actually read another one of Annie Duke's books, *Quit:
The Power of Knowing When to Walking Away*, a few years ago - highly recommend
her books. 

The impetus for this post came from the list entry I'm currently reading, Andrew
Lo's *Adaptive Markets*. It's been my favorite so far because it connects the
mathematical biology I studied in undergrad with mathematical finance in
surprising ways. Chapter 8's discussion of market efficiency introduces J. Doyne
Farmer, a polymath researcher who has contributed to chaos theory, biology, and
mathematical research in addition to founding one of the first quantitative
hedge funds, Prediction Company. 

Lo cites a 2009 paper by Dmitriy Cherkashin, J. Doyne Farmer, and Seth Lloyd in support
of the claim that market inefficiencies can persist for significant periods of
time due to the interaction of trading strategies in the market. He draws an
analogy to the Lotka-Volterra equations, a popular predator-prey model which
models how population sizes can oscillate over time rather than reaching a
single fixed point.

I first encountered the Lotka-Volterra equations in Darren Wilkinson's textbook,
*Stochastic Modeling for Systems Biology*. The interaction between predators and
prey introduces relatively simple non-linear terms, which, for the right initial
conditions, lead to oscillating populations of both predator and prey. The
intuition is that the predators depend on the prey in order to eat and be able
to reproduce; however, as the predators eat their prey, they drive the prey
population down and the predator population up until there aren't enough prey
for the predators to survive and reproduce. At this point, the predator
population decreases enough for the prey population to stabilize and grow. The
cycle repeats infinitely. Doyne showed a similar result for hedge fund
strategies, where the interaction of market participants
leads to boom and bust cycles for different strategies.

Returning to Cherkashin et. al.: their 2009 paper builds a simple betting game
to show that interactions between strategies can cause inefficiencies to persist
for long periods of time. The intuition here is that, depending on the setup,
there can be oscillations which last
long enough that they prevent a rational actor from quickly closing the
resulting inefficiency.

## Setting up the Reality Game ##

The paper proceeds by setting up an evolutionary game called (rather fancifully)
the Reality Game. They provide a general framework but focus on a coin flip
where the probability of heads at each time step is determined by a function of
the prior outcome referred to as the reality map. Players bet all of their
wealth each round with no house take, and the winners receive a portion of
the total pool relative to what they bet on the winning outcome
(i.e., pari-mutuel betting). 

Here's some notation from the paper:
- $N$ agents place wagers on $L$ possible outcomes. For a coin toss, $L=2$.
- $s_i$ is the amount of player $i$'s total wealth he or she wagers on heads (so, $1-s_i$ is their wager on
  tails).
- $w_i$ is the portion of the total wealth pool that player $i$ holds. Wealth is
  normalized so $\sum_i w_i = 1$.
- $p = \sum_i s_i w_i$ is the total amount bet on heads. Of course, $1-p$ is the
  total bet on tails.
- Supposing heads wins, $\pi_i = \frac{s_i w_i}{p}$ is the payout to player $i$.
  if tails wins, $\pi_i = \frac{(1-s_i)w_i}{1-p}$ is the payout.
- $q$ is the probability that heads wins. The reality map is the function
  $q(p)$.

Here's an interesting aside: if $q$ is a constant, the wealth updating rule is
analogous to Bayesian inference. In the below, the subscript $\lambda$ refers to
the winner of either heads or tails. So, $p_{\lambda} = p$ when heads wins and
$1-p$ when tails wins.

$$
w_i^{(t+1)} = \frac{s_{i\lambda} w_i^{(t)}}{p_{\lambda}}
$$

You can interpret the prior period wealth as the prior probability of heads and the next
period wealth as the posterior probability. Just as how Bayesian inference leads
to more and more accurate estimates of the true probability distribution, this
model causes players who probability match (i.e., they bet on each outcome
proportionally to its probability) to eventually accrue all of the wealth.

More generally, reality maps are characterized according to how they vary with
$p$:

- Objective, where $q(p) = const.$. Previous results don't affect the future
  probability of the game.
- Self-defeating, where $q'(p) < 0$. The more wealth bet on heads, the less
  likely it becomes in the next round.
- Self-reinforcing, where $q'(p) > 0$. The more wealth bet on heads, the more
  likely it becomes in the next round.
  - The special case of $q(p) = p$ is referred to as *purely subjective*, i.e.,
    the future probability of heads is exactly equal to what was previously bet
    on heads.

# Part One: Recreating Their Results #

Using the notation defined above, it's pretty simple to write a function which
simulates rounds of betting. I follow the paper's example of using 30 strategies
evenly spaced over $[0,1]$, where a strategy is just a value for $s_i$, the
portion of wealth bet on heads. The function returns the wealth distribution
and the values of the reality map over time.

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def simulations(N, T, realityMap):
    # N is the number of strategies, evenly spaced over [0,1]
    # T is the number of rounds to simulate
    # realityMap is the reality map, a function defining q

    # define strategies
    strategies = np.arange(1,N) / N

    # store wealth for each strategy
    wealth = np.zeros([T,N-1])
    wealth[0] = np.ones(N-1) / (N-1)

    # Initiate reality map
    q = np.zeros(T)
    q[0] = 0.5

    for i in range(1,T):
       # Calculate outcome
       outcome = random.random() < q[i-1]

       # Update Wealth
       betOnHeads = sum(strategies * wealth[i-1])
       if outcome:
           wealth[i] = [strategies[j] * wealth[i-1][j] for j in range(0,N-1)] / betOnHeads
       else:
           wealth[i] = [(1-strategies[j]) * wealth[i-1][j] for j in range(0,N-1)] / (1-betOnHeads)

       # update reality map
       q[i] = realityMap(betOnHeads)

    return q, wealth
```

The paper uses a family of arctangent-based functions for the reality maps,
along with simple self-defeating and self-reinforcing examples. The set of
functions used in figure 1 are below:

```python
# figure (a)
def selfDefeatingRM(p):
    return 1-p

# figure (b)
def figBRM(p):
    return 0.5 + np.arctan((np.pi * 0.5 * (p - 0.5))/(1 - (2*p - 1)**2)) / np.pi

# figure (c)
def subjectiveRM(p):
    return p

# figure (d)
def figDRM(p):
    return 0.5 + np.arctan((np.pi * 1.5 * (p - 0.5))/(1 - (2*p - 1)**2)) / np.pi

# figure (e)
def multiModalRM(p):
    return (3 * p) % 1 
```

See the paper itself for more details on why they chose that arctangent
function. With our simulation function and the reality maps defined, we can
recreate their Figure 1 showing how the reality maps $q(p)$ evolve.

```python
# Run and plot the simulations

fig, axs = plt.subplots(nrows=2, ncols=3, sharey='all')
x = np.arange(0,2000)
x_e = np.arange(0,10_000)
axs[0,0].set_title("1a (Self-Defeating)")
axs[0,1].set_title("1b (alpha = 0.5)")
axs[0,2].set_title("1c (Pure Subjective)")
axs[1,0].set_title("1d (alpha = 1.5)")
axs[1,1].set_title("1e (Multi-Modal)")

for i in range(0,30):
    a_q, a_wealth = simulations(30, 2000, selfDefeatingRM)
    b_q, b_wealth = simulations(30, 2000, figBRM)
    c_q, c_wealth = simulations(30, 2000, subjectiveRM)
    d_q, d_wealth = simulations(30, 2000, figDRM)
    e_q, e_wealth = simulations(30, 10_000, multiModalRM)

    axs[0,0].plot(x,a_q)
    axs[0,1].plot(x,b_q)
    axs[0,2].plot(x,c_q)
    axs[1,0].plot(x,d_q)
    axs[1,1].plot(x_e,e_q, linewidth=0.1, linestyle='dotted')

plt.show()
```

In the figures below, the x-axis is the number of rounds that have been played
and the y-axis is the value of $q(p)$. The different colored lines represent
different simulation instances.

![Figure 1](/assets/realityGame/Figure_1.png)

My results match the qualitative behavior shown in the paper. (a) and (b) show
the probability moving towards the fixed point $q(p) = 0.5$, more quickly in (a)
than in (b). (c) is interesting - the steady state is determined by the first
several dice rolls, as they shift wealth towards a particular probability of
heads which quickly cements itself as wealth concentrates in the strategies near
that probability. (d) is a less extreme example of a self-reinforcing reality
map; $q(p)$ heads towards the fixed points of either 1 or 0, though in some
instances it does so very slowly. 

My multi-modal graph is difficult to read; I tried reducing the line width and
making it dotted to make it easier, but the wild oscillations between 1 and 0
give a result a bit like when I tried to mix paints in first grade - it just
comes out muddy and unclear. Looking under the hood, however, I'm seeing the
same behavior the paper reported. Wealth becomes concentrated at strategies $s =
1/3$ and $s = 2/3$, the discontinuities in the reality map. 

# Extending to a Dice Roll #

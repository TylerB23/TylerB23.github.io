---
layout: post
title: "Translating the Gillespie Algorithm from Python to Ocaml, pt. 1"
date: 2020-05-13
categories: python ocaml coding
excerpt: "First, let's explain the algorithm and implementing it in Python."
header:
  overlay_image: assets/tubes.jpg
  overlay_filter: 0
---
## Introduction ##
This semester, I took a class called "Applied Probability and Stochastic
Processes for Biology", which is cross-listed across seven departments. The
class was a mixture of undergrads and graduate students. That's always a fun
time -- graduate students tend to be less shy about asking questions than
undergrads, and in a class as interdisciplinary as this one, I doubt anyone but
the professor came in with all of the helpful background.

Anyways, one of the departments this class was listed under was Electrical
Engineering and Computer Science, largely because of its emphasis on numerical
simulation tools. The most elementary of these is the [Gillespie Algorithm][GA],
introduced by Daniel Gillespie in his 1977 paper *Exact Stochastic Simulation of
Coupled Chemical Reactions*. The basic idea is this:

Chemical reactions occur when the right combination of molecules bump into each
other in the correct orientation with sufficient speed. If we had an incredibly
powerful computer, we could simulate the exact movements, orientations, and
speeds of all the molecules in an area and get an exact, deterministic
simulation of the system. This, however, is unfeasible for a system of any level
of complexity. Instead, the most common approach is to approximate these
reactions by simplifying our simulation.

For very, very large systems, we don't care very much about the individual
reactions occuring at any point in time. Instead we care about the general rate
at which the system reacts and the overall time it takes to complete. If you've
taken introductory chemistry or differential equations, you may be familiar with
rate laws used to describe reactions in such large systems. As an overview, 
consider a reaction $aA + bB \rightarrow P$, where $P$ is a stand-in for 
reaction products. The rate law is
$rate = k[A]^x[B]^y$, where $x$ and $y$ are the order with respect to
species A and B, respectively. The order is experimentally determined, and can
be an integer or a non-integer depending on the complexity of the system.
Chemical kinetics are a complex field -- there's a nice overview at
[libretexts]. The rate law becomes a system of coupled differential equations
that look something like

$$
\begin{gather*}
    \frac{dA}{dt} = f_A(A,B) \\
    \frac{dB}{dt} = f_B(A,B)
\end{gather*}
$$

As Gillespie notes in the abstract of his paper, this is not as physically
meaningful as a stochastic formulation, where individual reactions are tracked
and occur with randomly distributed rates. To make this formulation tractable, 
Gillespie provides a wonderful, relatively simple to follow derivation of his
algorithm in the paper linked above. I'll skip over the fine details and present
you with the Wikipedia version:
1. Initialise the number of species, the total time to run the simulation,
   and your random number generator (if need be).
2. For each reaction, compute a time interval and choose a reaction. This is
   done based upon the hazard functions of the individual reactions, which
   are similar to their rate laws (though not exactly the same).
3. Update the species counts and the time.
4. Repeat until the time allotted runs out or no reactions are possible (go back
   to step 2).

The algorithm is exact and stochastic in that it draws a time between reactions
and a specific reaction from a probability distribution based on the hazard
functions, which describe how likely an individual reaction is to occur. 
While expensive, this was a major step forward in stochastic
simulations of such systems. It can be used to approximate any system which
resembles chemical reactions -- in class, we used it to represent population
dynamics like Lotka-Volterra, and epidemic models like the SIR model, for
example.

## Python Implementation ##

The best way to understand the algorithm is to see an implementation. Let's
consider a simple dimerisation, where two species react to form a dimer which
can decompose back into the species.

$$
\begin{gather}
    A + B \xrightarrow{h_1} C \\
    C \xrightarrow{h_2} A + B
\end{gather}
$$

Where $h_1 = k_1 A B$ and $h_2 = k_2 C$ are the hazard functions of their
respective reactions. I've implemented the algorithm in Python as a
demonstration:
[python code](/assets/gillespie_example.py)

{% highlight python %}
import numpy as np
from random import uniform
import matplotlib.pyplot as plt

def gillespie(T, N_a, N_b, N_c, k1, k2):
    # N_i are the initial counts of A, B, and C
    # T is the toal time to run the simulation
    #k1 and k2 are the hazard constants

    # Initialisations
    t = 0
    A = N_a
    B = N_b
    C = N_c
    particles = [(A,B,C,t)] # array captures system state at time t as tuple

    # Iterations
    while(t < T):
        # Calculate hazards
        h1 = k1 * A * B
        h2 = k2 * C
        htotal = h1 + h2
        # Draw wait time
        w = uniform(0,1)
        t_wait = (-1 / htotal) * np.log(1 - w)
        # Choose reaction
        pvec = np.array([h1, h2]) / htotal # normalised probability vector
        rxn = 1 + np.random.binomial(1, pvec[1])
        if rxn == 1:
            A = A - 1
            B = B - 1
            C = C + 1
        elif rxn == 2:
            A = A + 1
            B = B + 1
            C = C - 1
        # Iterate counters
        t = t + t_wait
        particles.append((A,B,C,t))

    return particles
{% endhighlight %}

So here's the idea: while I spend the month of May waiting to begin my summer
plans, I thought it would be fun to learn some OCaml. OCaml is a general purpose
programming language with a nice type system which helps prevent errors and
makes code 'safer' in that it can be quickly written with fewer errors. A lot of
big companies including Facebook and Citrix use it, as well as financial groups
like Bloomberg and Jane Street. I looked at some tutorials on the language a few
weeks back, and was struck by how odd looking it was compared to what I'm used
to working in. Since the Gillespie algorithm is fresh in my head, I thought it
would be a more fun place to start than the typical searching-and-sorting fare.
So this will be the first in a series of blog posts, as I learn more about
OCaml, try to translate that on here, and then begin to implement some of my
past Python projects from Stochastics class into OCaml. Stay tuned!

[GA]: https://doi.org/10.1021/j100540a008
[libretexts]: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Kinetics/Rate_Laws/The_Rate_Law/Reaction_Order

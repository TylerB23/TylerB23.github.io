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

import numpy as np
import matplotlib.pyplot as plt

def GW(p0, p1, z0, T, plot = True):
    # p0 is probability of 0 progeny
    # p1 is probability of 1 progeny
    # z0 is initial particle count
    # T is time to run. Note each time step is a generation
    
    p2 = 1 - (p0 + p1) # chance of 2 progeny
    pvec = [p0, p1, p2]
    t = 0
    z = z0 # current particle counter
    particles = [z]

    while(t < T):
        progeny = np.random.multinomial(z, pvec)
        z = 0*progeny[0] + 1*progeny[1] + 2*progeny[2]
        particles.append(z)
        t += 1
    
    if plot:
        plt.plot(particles)
        plt.show()

    return particles

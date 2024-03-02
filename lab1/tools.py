import numpy as np
import matplotlib.pyplot as plt

def white_noise(n_series, length, mean=0, std=1):
    return mean + std * np.random.randn(n_series, length)

def random_walk(WN):
    return np.cumsum(WN, axis=0)

def gauss_markov(WN, tau, dt=1): 
    length = WN.shape[1]
    beta=1/tau
    GM = np.zeros_like(WN) # Assume GM[0] = 0
    for i in range(1, length):
        GM[:,i] = GM[:,i-1] * np.exp(-beta*dt)+ WN[:,i-1]
    return GM
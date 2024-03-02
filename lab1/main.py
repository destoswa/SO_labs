from tools import *
import matplotlib.pyplot as plt

# 1. Generate white noise (3 x 200'000)
std = 2
freq=1
dt = 1/freq
length = int(2e5)
n_series = 3
WN = white_noise(n_series=n_series, length=length, std=std)

# 2. Generate random walk (3 x 200'000) from WN
RW = random_walk(WN)

# 3. Generate 1st order Gauss Markov process
GM_2000 = gauss_markov(WN, tau=2000, dt=1)
GM_500 =  gauss_markov(WN, tau=500, dt=1)

# Figure 1
fig, axs = plt.subplots(4,1, constrained_layout = True, figsize=(10,10))

# A. 3 WN realization with different color and legends
axs[0].plot(WN.T, linewidth=0.01)
axs[0].title.set_text('White noises')

# B. 3 RW realization with different color and legends
axs[1].plot(RW.T, linewidth=0.01)
axs[1].title.set_text('Random walks')

# C. 3 GM (T=2000) realization with different color and legends
axs[2].plot(GM_2000.T, linewidth=lw)
axs[2].title.set_text('1st order Gauss-Markov process, tau = 2000')

# D. 3 GM (T=500) realization with different color and legends
axs[3].plot(GM_500.T, linewidth=lw)
axs[3].title.set_text('1st order Gauss-Markov process, tau = 500')

fig.suptitle('FIG 1 : !! ADD LEGEND !!', fontsize=16)
fig.savefig('Fig_1.eps',format ='eps')
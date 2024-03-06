import numpy as np
import matplotlib.pyplot as plt
from tools import *


def main():
    WN = white_noise(n_series=1, length=int(1e5), std=2)
    RW = random_walk(WN)

    tau1, av1 = AVar(WN[0,:])
    av2 = AVar(RW[0,:])
    av3 = AVar((WN + RW)[0,:])
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    axs[0].loglog(tau1, av1)
    axs[1].loglog(av2[0], av2[1])
    axs[2].loglog(av3[0], av3[1])
    plt.show()


if __name__ == '__main__':
    main()

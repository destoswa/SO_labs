import numpy as np
import matplotlib.pyplot as plt
from tools import *


def main():
    # ===========================================
    # =========== PART A ========================
    # ===========================================
    #  1. Generate white noise (3 x 200'000)
    std = 2
    lw = 1.0
    freq = 1
    dt = 1/freq
    length = int(2e5)
    n_series = 3
    WN = white_noise(n_series=n_series, length=length, std=std)

    # 2. Generate random walk (3 x 200'000) from WN
    RW = random_walk(n_series=n_series, length=length, std=std)

    # 3. Generate 1st order Gauss Markov process
    GM_2000 = gauss_markov(n_series=n_series, length=length, tau=2000, std=std, dt=1)
    GM_500 = gauss_markov(n_series=n_series, length=length, tau=500, std=std, dt=1)

    # Figure 1
    fig, axs = plt.subplots(4, 1, constrained_layout=True, figsize=(10, 10))

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

    fig.suptitle('FIG 1 : !! ADD LEGEND !!', fontsize=16.0)
    #plt.show()
    fig.savefig('Fig_1.svg', format='svg')
    fig.savefig('Fig_1.png', format='png')

    # saving results in .txt file
    np.savetxt('WN.txt', WN.T, delimiter=';', fmt='%.8f')
    np.savetxt('RW.txt', RW.T, delimiter=';', fmt='%.8f')
    np.savetxt('GM_2000.txt', GM_2000.T, delimiter=';', fmt='%.8f')
    np.savetxt('GM_500.txt', GM_500.T, delimiter=';', fmt='%.8f')

    # ===========================================
    # =========== PART B ========================
    # ===========================================
    # 4. Noise characteristics for each sequence
    # 4.a AutoCorrelation
    do_ac = False
    if do_ac == True:
        fig, axs = plt.subplots(4, 1)
        fig.suptitle('AutoCorrelation')
        # A. AC of 3 WN realization with different color and legends
        for i in range(n_series):
            AC_WN = AC(WN[i, :])
            AC_WN = (AC_WN - np.min(AC_WN)) / (np.max(AC_WN) - np.min(AC_WN))
            axs[0].plot(AC_WN)
            axs[0].set_title(f"White Noise")

        # B. AC of 3 RW realization with different color and legends
        for i in range(n_series):
            AC_RW = AC(RW[i, :])
            AC_RW = (AC_RW - np.min(AC_RW)) / (np.max(AC_RW) - np.min(AC_RW))
            axs[1].plot(AC_RW)
            axs[1].set_title(f"Random Walk")

        # C. AC of 3 GM (T=2000) realization with different color and legends
        for i in range(n_series):
            AC_GM_2000 = AC(GM_2000[i, :])
            AC_GM_2000 = (AC_GM_2000 - np.min(AC_GM_2000)) / (np.max(AC_GM_2000) - np.min(AC_GM_2000))
            axs[2].plot(AC_GM_2000)
            axs[2].set_title(f"Gauss Markov - tau=2000")

        # D. AC of 3 GM (T=500) realization with different color and legends
        for i in range(n_series):
            AC_GM_500 = AC(GM_500[i, :])
            AC_GM_500 = (AC_GM_500 - np.min(AC_GM_500)) / (np.max(AC_GM_500) - np.min(AC_GM_500))
            axs[3].plot(AC_GM_500)
            axs[3].set_title(f"Gauss Markov - tau=500")
        plt.tight_layout()
        fig.savefig('AC.svg', format='svg')
        fig.savefig('AC.png', format='png')
        plt.show()

    # 4.b Power-Spectral_Density
    frac = None
    do_psd = True
    if do_psd == True:
            fig, axs = plt.subplots(4, 1)
            fig.suptitle('Power Spectral Density')
            # A. AC of 3 WN realization with different color and legends
            for i in range(n_series):
                (f1, S1) = PSD(WN[i, :frac])
                axs[0].plot(f1, S1)
                axs[0].set_title(f"White Noise")

            # B. AC of 3 RW realization with different color and legends
            for i in range(n_series):
                (f2, S2) = PSD(RW[i, :frac])
                axs[1].plot(f2, S2)
                axs[1].set_title(f"Random Walk")

            # C. AC of 3 GM (T=2000) realization with different color and legends
            for i in range(n_series):
                (f3, S3) = PSD(GM_2000[i, :frac])
                axs[2].plot(f3, S3)
                axs[2].set_title(f"Gauss Markov - tau=2000")

            # D. AC of 3 GM (T=500) realization with different color and legends
            for i in range(n_series):
                (f4, S4) = PSD(GM_500[i, :frac])
                axs[3].plot(f4, S4)
                axs[3].set_title(f"Gauss Markov - tau=500")
            plt.tight_layout()
            fig.savefig('PSD.svg', format='svg')
            fig.savefig('PSD.png', format='png')
            plt.show()

    # 4.c Allan Variance
    frac = None
    do_av = False
    if do_av == True:
            fig, axs = plt.subplots(4, 1)
            fig.suptitle('Allan Variance')
            # A. AC of 3 WN realization with different color and legends
            #(f1, S1) = PSD(WN[0, :frac])
            a = AVar(WN[0, :])
            axs[0] = allantools.Plot()
            axs[0].plot(a, errorbars=True, grid=True)
            axs[0].ax.set_title(f"White Noise")

            # B. AC of 3 RW realization with different color and legends
            #(f2, S2) = PSD(RW[0, :frac])
            a = AVar(RW[0, :])
            axs[1] = allantools.Plot()
            axs[1].plot(a, errorbars=True, grid=True)
            axs[1].ax.set_title(f"Random Walk")

            # C. AC of 3 GM (T=2000) realization with different color and legends
            #(f3, S3) = PSD(GM_2000[0, :frac])
            a = AVar(GM_2000[0, :])
            axs[2] = allantools.Plot()
            axs[2].plot(a, errorbars=True, grid=True)
            axs[2].ax.set_title(f"Gauss Markov - tau=2000")

            # D. AC of 3 GM (T=500) realization with different color and legends
            a = AVar(GM_500[0, :])
            axs[3] = allantools.Plot()
            axs[3].plot(a, errorbars=True, grid=True)
            axs[3].ax.set_title(f"Gauss Markov - tau=500")
            plt.tight_layout()
            fig.savefig('AVar.svg', format='svg')
            fig.savefig('AVar.png', format='png')
            plt.show()


if __name__ == '__main__':
    main()

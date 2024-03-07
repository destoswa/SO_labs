import matplotlib.pyplot as plt
from tools import *



def main():

	# paths
	REALIZATION_FOLDER = "./data/realizations/"
	IMAGES_FOLDER = "./data/images/"

	# hyper-param
	frac = None
	do_ac = True
	do_psd = True
	do_av = True
	do_savefig = True

	# ===========================================
	# =========== PART A ========================
	# ===========================================
	# 1. Generate white noise (3 x 200'000)
	std = 2
	length = int(2e5)
	n_series = 3
	wn = white_noise(n_series=n_series, length=length, std=std)

	# 2. Generate random walk (3 x 200'000) from WN
	rw = random_walk(wn)

	# 3. Generate 1st order Gauss Markov process
	gm_2000 = gauss_markov(wn, tau=2000, dt=1)
	gm_500 = gauss_markov(wn, tau=500, dt=1)

	# Figure 1
	fig, axs = plt.subplots(4, 1, constrained_layout=True, figsize=(10, 10))

	# A. 3 WN realization with different color and legends
	axs[0].plot(wn.T, linewidth=0.01)
	axs[0].title.set_text('White noises')

	# B. 3 RW realization with different color and legends
	axs[1].plot(rw.T)
	axs[1].title.set_text('Random walks')

	# C. 3 GM (T=2000) realization with different color and legends
	axs[2].plot(gm_2000.T)
	axs[2].title.set_text('1st order Gauss-Markov process, tau = 2000')

	# D. 3 GM (T=500) realization with different color and legends
	axs[3].plot(gm_500.T)
	axs[3].title.set_text('1st order Gauss-Markov process, tau = 500')
	legend = ['Real 1', 'Real 2', 'Real 3']
	axs[3].legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

	fig.suptitle('Types of noises', fontsize=16.0)
	if do_savefig:
		fig.savefig(IMAGES_FOLDER + 'Fig_1.svg', format='svg')
		fig.savefig(IMAGES_FOLDER + 'Fig_1.png', format='png')

	# saving results in .txt file
	np.savetxt(REALIZATION_FOLDER + 'WN.txt', wn.T, delimiter=';', fmt='%.8f')
	np.savetxt(REALIZATION_FOLDER + 'RW.txt', rw.T, delimiter=';', fmt='%.8f')
	np.savetxt(REALIZATION_FOLDER + 'GM_2000.txt', gm_2000.T, delimiter=';', fmt='%.8f')
	np.savetxt(REALIZATION_FOLDER + 'GM_500.txt', gm_500.T, delimiter=';', fmt='%.8f')

	# ===========================================
	# =========== PART B ========================
	# ===========================================
	# 4. Noise characteristics for each sequence
	# 4.a AutoCorrelation
	if do_ac:
		fig, axs = plt.subplots(4, 1, constrained_layout=True, figsize=(10, 10))
		fig.suptitle('AutoCorrelation')
		# A. AC of 3 WN realization with different color and legends
		for i in range(n_series):
			ac_wn = autocorr(wn[i, :frac])
			ac_wn = (ac_wn - np.min(ac_wn)) / (np.max(ac_wn) - np.min(ac_wn))
			axs[0].plot(ac_wn)
		axs[0].set_title(f"White Noise")

		# B. AC of 3 RW realization with different color and legends
		for i in range(n_series):
			ac_rw = autocorr(rw[i, :frac])
			ac_rw = (ac_rw - np.min(ac_rw)) / (np.max(ac_rw) - np.min(ac_rw))
			axs[1].plot(ac_rw)
		axs[1].set_title(f"Random Walk")

		# C. AC of 3 GM (T=2000) realization with different color and legends
		for i in range(n_series):
			ac_gm_2000 = autocorr(gm_2000[i, :frac])
			ac_gm_2000 = (ac_gm_2000 - np.min(ac_gm_2000)) / (np.max(ac_gm_2000) - np.min(ac_gm_2000))
			axs[2].plot(ac_gm_2000)
		axs[2].set_title(f"Gauss Markov - tau=2000")

		# D. AC of 3 GM (T=500) realization with different color and legends
		for i in range(n_series):
			ac_gm_500 = autocorr(gm_500[i, :frac])
			ac_gm_500 = (ac_gm_500 - np.min(ac_gm_500)) / (np.max(ac_gm_500) - np.min(ac_gm_500))
			axs[3].plot(ac_gm_500)
		axs[3].set_title(f"Gauss Markov - tau=500")
		legend = ['Real 1', 'Real 2', 'Real 3']
		axs[3].legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

		if do_savefig:
			fig.savefig(IMAGES_FOLDER + 'AC.svg', format='svg')
			fig.savefig(IMAGES_FOLDER + 'AC.png', format='png')

	# 4.b Power-Spectral_Density
	if do_psd:
		fig, axs = plt.subplots(4, 1, constrained_layout=True, figsize=(10, 10))
		fig.suptitle('Power Spectral Density')
		# A. AC of 3 WN realization with different color and legends
		for i in range(n_series):
			(f1, S1) = psd(wn[i, :frac])
			axs[0].plot(f1, S1)
		axs[0].set_title(f"White Noise")

		# B. AC of 3 RW realization with different color and legends
		for i in range(n_series):
			(f2, S2) = psd(rw[i, :frac])
			axs[1].plot(f2, S2)
		axs[1].set_title(f"Random Walk")

		# C. AC of 3 GM (T=2000) realization with different color and legends
		for i in range(n_series):
			(f3, S3) = psd(gm_2000[i, :frac])
			axs[2].plot(f3, S3)
		axs[2].set_title(f"Gauss Markov - tau=2000")

		# D. AC of 3 GM (T=500) realization with different color and legends
		for i in range(n_series):
			(f4, S4) = psd(gm_500[i, :frac])
			axs[3].plot(f4, S4)
		axs[3].set_title(f"Gauss Markov - tau=500")
		legend = ['Real 1', 'Real 2', 'Real 3']
		axs[3].legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

		if do_savefig:
			fig.savefig(IMAGES_FOLDER + 'PSD.svg', format='svg')
			fig.savefig(IMAGES_FOLDER + 'PSD.png', format='png')

	# 4.c Allan Variance
	if do_av:
		fig, axs = plt.subplots(4, 1, constrained_layout=True, figsize=(10, 10))
		fig.suptitle('Allan Variance')
		# A. AC of 3 WN realization with different color and legends
		tau, av = allan_var(wn[0, :])
		axs[0].loglog(tau, av)
		axs[0].set_title(f"White Noise")

		# B. AC of 3 RW realization with different color and legends
		tau, av = allan_var(rw[0, :])
		axs[1].loglog(tau, av)
		axs[1].set_title(f"Random Walk")

		# C. AC of 3 GM (T=2000) realization with different color and legends
		tau, av = allan_var(gm_2000[0, :])
		axs[2].loglog(tau, av)
		axs[2].set_title(f"Gauss Markov - tau=2000")

		# D. AC of 3 GM (T=500) realization with different color and legends
		tau, av = allan_var(gm_500[0, :])
		axs[3].loglog(tau, av)
		axs[3].set_title(f"Gauss Markov - tau=500")
		if do_savefig:
			fig.savefig(IMAGES_FOLDER + 'AVar.svg', format='svg')
			fig.savefig(IMAGES_FOLDER + 'AVar.png', format='png')

	plt.show()


# 6.


if __name__ == '__main__':
	main()

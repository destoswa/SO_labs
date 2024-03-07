from tools import *


def main():
	# paths
	IMAGES_FOLDER = "./data/images/"

	# hyper-param
	random_seed = 42
	wn_std = 2
	length = int(2e5)
	n_series = 3
	LEGEND = ['Real '+str(i+1) for i in range(n_series)]

	# flags
	do_ac = True
	do_psd = True
	do_av = True
	do_savefig = True

	# ===========================================
	# =========== PART A ========================
	# ===========================================

	fig, axs = create_subfigs(title='Type of noises', shape=(4, 1))

	# A. 3 WN realization with different color and legends
	wn = white_noise(n_series=n_series, length=length, std=wn_std, random_seed=random_seed)
	plot_1(ax=axs[0], serie=wn, title='White noises', legend=LEGEND, linewidth=0.1)

	# B. 3 RW realization with different color and legends
	rw = random_walk(wn)
	plot_1(ax=axs[1], serie=rw, title='Random walks', legend=LEGEND)

	# C. 3 GM (T=2000) realization with different color and legends
	gm_2000 = gauss_markov(wn, tau=2000, dt=1)
	plot_1(ax=axs[2], serie=gm_2000, title='1st order Gauss-Markov process, tau = 2000', legend=LEGEND)

	# D. 3 GM (T=500) realization with different color and legends
	gm_500 = gauss_markov(wn, tau=500, dt=1)
	plot_1(ax=axs[3], serie=gm_500, title='1st order Gauss-Markov process, tau = 500', legend=LEGEND)

	if do_savefig:
		save_fig(fig=fig, name='Fig_1', folder=IMAGES_FOLDER)

	# ===========================================
	# =========== PART B ========================
	# ===========================================
	# 4. Noise characteristics for each sequence
	# 4.a AutoCorrelation
	if do_ac:
		fig, axs = create_subfigs(title='AutoCorrelation', shape=(4, 1))
		x = range(-length + 1, length)

		# A. AC of 3 WN realization with different color and legends
		ac_wn = [autocorr_norm(wn[i]) for i in range(n_series)]
		plot_ac(ax=axs[0], x=x, serie=ac_wn, title='White Noise', legend=LEGEND)

		# B. AC of 3 RW realization with different color and legends
		ac_rw = [autocorr_norm(rw[i]) for i in range(n_series)]
		plot_ac(ax=axs[1], x=x, serie=ac_rw, title='Random Walk', legend=LEGEND)

		# C. AC of 3 GM (T=2000) realization with different color and legends
		ac_gm_2000 = [autocorr_norm(gm_2000[i]) for i in range(n_series)]
		plot_ac(ax=axs[2], x=x, serie=ac_gm_2000, title='Gauss Markov - tau=2000', legend=LEGEND)

		# D. AC of 3 GM (T=500) realization with different color and legends
		ac_gm_500 = [autocorr_norm(gm_500[i]) for i in range(n_series)]
		plot_ac(ax=axs[3], x=x, serie=ac_gm_500, title='Gauss Markov - tau=500', legend=LEGEND)

		if do_savefig:
			save_fig(fig=fig, name='AC', folder=IMAGES_FOLDER)

	# 4.b Power-Spectral_Density
	if do_psd:
		fig, axs = create_subfigs(title="Power Spectral Density", shape=(4, 1))

		# A. AC of 3 WN realization with different color and legends
		wn_psd = [psd(wn[i]) for i in range(n_series)]
		plot_psd(ax=axs[0], psd=wn_psd, title='White Noise', legend=LEGEND)

		# B. AC of 3 RW realization with different color and legends
		rw_psd = [psd(rw[i]) for i in range(n_series)]
		plot_psd(ax=axs[1], psd=rw_psd, title='Random Walk', legend=LEGEND)

		# C. AC of 3 GM (T=2000) realization with different color and legends
		gm_2000_psd = [psd(gm_2000[i]) for i in range(n_series)]
		plot_psd(ax=axs[2], psd=gm_2000_psd, title='Gauss Markov - tau=2000', legend=LEGEND)

		# D. AC of 3 GM (T=500) realization with different color and legends
		gm_500_psd = [psd(gm_500[i]) for i in range(n_series)]
		plot_psd(ax=axs[3], psd=gm_500_psd, title='Gauss Markov - tau=500', legend=LEGEND)

		if do_savefig:
			save_fig(fig=fig, name='PSD', folder=IMAGES_FOLDER)

	# 4.c Allan Variance
	if do_av:
		fig, axs = create_subfigs(title='Allan Variance', shape=(4, 1))

		# A. AC of 3 WN realization with different color and legends
		tau, av = allan_var(wn[0])
		plot_loglog_av(ax=axs[0], tau=tau, av=av, title='White Noise', legend=LEGEND[0])

		# B. AC of 3 RW realization with different color and legends
		tau, av = allan_var(rw[0])
		plot_loglog_av(ax=axs[1], tau=tau, av=av, title='Random Walk', legend=LEGEND[0])

		# C. AC of 3 GM (T=2000) realization with different color and legends
		tau, av = allan_var(gm_2000[0])
		plot_loglog_av(ax=axs[2], tau=tau, av=av, title='Gauss Markov - tau=2000', legend=LEGEND[0])

		# D. AC of 3 GM (T=500) realization with different color and legends
		tau, av = allan_var(gm_500[0])
		plot_loglog_av(ax=axs[3], tau=tau, av=av, title='Gauss Markov - tau=500', legend=LEGEND[0])

		if do_savefig:
			save_fig(fig=fig, name='AVar', folder=IMAGES_FOLDER)

	plt.show()

# 6.


if __name__ == '__main__':
	main()

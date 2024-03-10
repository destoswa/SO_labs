from tools import *


def main():
	# hyper-param
	random_seed = 404
	wn_mean = 0
	wn_std = 2
	length = int(2e5)
	n_series = 3
	LEGEND = ['Real ' + str(i + 1) for i in range(n_series)]

	# flags
	do_ac = True
	do_psd = True
	do_av = True
	do_savefig = True

	fig, axs = create_subfigs(title='Type of noises', shape=(4, 1))

	# 1. 3 WN realization with different color and legends
	wn = white_noise(n_series=n_series, length=length, mean=wn_mean, std=wn_std, random_seed=random_seed)
	plot_1(ax=axs[0], serie=wn, title='White noises', legend=LEGEND, linewidth=0.1)

	# 2. 3 RW realization with different color and legends
	rw = random_walk(wn)
	plot_1(ax=axs[1], serie=rw, title='Random walks', legend=LEGEND)

	# 3a. 3 GM (T=2000) realization with different color and legends
	gm_2000 = gauss_markov(wn, tau=2000, dt=1)
	plot_1(ax=axs[2], serie=gm_2000, title='1st order Gauss-Markov process, tau = 2000', legend=LEGEND)

	# 3b. 3 GM (T=500) realization with different color and legends
	gm_500 = gauss_markov(wn, tau=500, dt=1)
	plot_1(ax=axs[3], serie=gm_500, title='1st order Gauss-Markov process, tau = 500', legend=LEGEND)

	# save results
	if do_savefig:
		save_fig(fig=fig, name='Fig_1')

	save_realization(name='WN', serie=wn)
	save_realization(name='RW', serie=rw)
	save_realization(name='GM_2000', serie=gm_2000)
	save_realization(name='GM_500', serie=gm_500)

	# 4. Noise characteristics for each sequence
	# 4.a AutoCorrelation
	if do_ac:
		fig, axs = create_subfigs(title='AutoCorrelation', shape=(4, 1))
		x = range(-length + 1, length)

		# A. AC of 3 WN realization with different color and legends
		ac_wn = [autocorr(wn[i]) for i in range(n_series)]
		plot_ac(ax=axs[0], x=x, serie=ac_wn, title='White Noise', legend=LEGEND)

		# B. AC of 3 RW realization with different color and legends
		ac_rw = [autocorr(rw[i]) for i in range(n_series)]
		plot_ac(ax=axs[1], x=x, serie=ac_rw, title='Random Walk', legend=LEGEND)

		# C. AC of 3 GM (T=2000) realization with different color and legends
		ac_gm_2000 = [autocorr(gm_2000[i]) for i in range(n_series)]
		plot_ac(ax=axs[2], x=x, serie=ac_gm_2000, title='Gauss Markov - tau=2000', legend=LEGEND)

		# D. AC of 3 GM (T=500) realization with different color and legends
		ac_gm_500 = [autocorr(gm_500[i]) for i in range(n_series)]
		plot_ac(ax=axs[3], x=x, serie=ac_gm_500, title='Gauss Markov - tau=500', legend=LEGEND)

		if do_savefig:
			save_fig(fig=fig, name='AC')

	# 4.b Power-Spectral_Density
	if do_psd:
		fig, axs = create_subfigs(title="Power Spectral Density", shape=(4, 1))

		# A. AC of 3 WN realization with different color and legends
		wn_psd = [psd(wn[i]) for i in range(n_series)]
		plot_psd(ax=axs[0], serie=wn_psd, title='White Noise', legend=LEGEND)

		# B. AC of 3 RW realization with different color and legends
		rw_psd = [psd(rw[i]) for i in range(n_series)]
		plot_psd(ax=axs[1], serie=rw_psd, title='Random Walk', legend=LEGEND)

		# C. AC of 3 GM (T=2000) realization with different color and legends
		gm_2000_psd = [psd(gm_2000[i]) for i in range(n_series)]
		plot_psd(ax=axs[2], serie=gm_2000_psd, title='Gauss Markov - tau=2000', legend=LEGEND)

		# D. AC of 3 GM (T=500) realization with different color and legends
		gm_500_psd = [psd(gm_500[i]) for i in range(n_series)]
		plot_psd(ax=axs[3], serie=gm_500_psd, title='Gauss Markov - tau=500', legend=LEGEND)

		if do_savefig:
			save_fig(fig=fig, name='PSD')

	# 4.c Allan Variance
	if do_av:
		fig, axs = create_subfigs(title='Allan Variance', shape=(4, 1))
		legend = ['Real 1']

		# A. AC of 3 WN realization with different color and legends
		tau, av = allan_var(wn[0])
		plot_loglog_av(ax=axs[0], tau=tau, av=av, title='White Noise', legend=legend)

		# B. AC of 3 RW realization with different color and legends
		tau, av = allan_var(rw[0])
		plot_loglog_av(ax=axs[1], tau=tau, av=av, title='Random Walk', legend=legend)

		# C. AC of 3 GM (T=2000) realization with different color and legends
		tau, av = allan_var(gm_2000[0])
		plot_loglog_av(ax=axs[2], tau=tau, av=av, title='Gauss Markov - tau=2000', legend=legend)

		# D. AC of 3 GM (T=500) realization with different color and legends
		tau, av = allan_var(gm_500[0])
		plot_loglog_av(ax=axs[3], tau=tau, av=av, title='Gauss Markov - tau=500', legend=legend)

		if do_savefig:
			save_fig(fig=fig, name='AVar')

	# 5. With realization 1

	# 5a White Noise parameters : std and mean of the white noise
	wn_measured_mean = np.mean(wn[0])
	wn_measured_std = np.std(wn[0])

	print()
	print(f'Statistics about white noise realization 1 : ')
	print(f'True mean = {wn_mean}, measured wn mean = {wn_measured_mean}')
	print(f'True std = {wn_std}, measured wn std = {wn_measured_std}')

	# 5b Random Walk
	# RW(t) = RW(t-1) + WN[t-1]
	rw_wn = rw[0, 1:] - rw[0, :-1]
	rw_wn_mean = np.mean(rw_wn)
	rw_wn_std = np.std(rw_wn)

	print()
	print(f'Statistics about random_walk realization 1 : ')
	print(f'True wn mean = {wn_mean}, measured wn mean = {rw_wn_mean}')
	print(f'True wn std = {wn_std}, measured wn std = {rw_wn_std}')

	# 5c 1st order Gauss-Markov tau=2000 process parameters, white noise mean and std + correlation time
	# GM[t] = GM[t-1]*exp(-beta*dt)+ WN[t-1]
	tau = find_gm_tau_from_ac(ac_gm_2000[0])  # tau derived from plot
	beta = 1 / tau
	dt = 1

	gm_2000_wn = gm_2000[0, 1:] - gm_2000[0, :-1] * np.exp(-beta * dt)
	gm_2000_wn_mean = np.mean(gm_2000_wn)
	gm_2000_wn_std = np.std(gm_2000_wn)

	print()
	print(f'Statistics about Gauss-Markov_tau2000 realization 1 : ')
	print(f'True tau = {2000}, tau derived from autocorelation (tau = x s.t. y[x]=y[0]*exp(-1)) = {tau}')
	print(f'True wn mean = {wn_mean}, measured wn mean = {gm_2000_wn_mean}')
	print(f'True wn std = {wn_std}, measured wn std = {gm_2000_wn_std}')

	# 5d 1st order Gauss-Markov tau=500 process parameters, white noise mean and std + correlation time
	# GM[t] = GM[t-1]*exp(-beta*dt)+ WN[t]

	tau = find_gm_tau_from_ac(ac_gm_500[0])  # tau derived from plot
	beta = 1 / tau
	dt = 1

	gm_500_wn = gm_500[0, 1:] - gm_500[0, :-1] * np.exp(-beta * dt)
	gm_500_wn_mean = np.mean(gm_500_wn)
	gm_500_wn_std = np.std(gm_500_wn)
	print()
	print(f'Statistics about Gauss-Markov_tau500 realization 1 : ')
	print(f'True tau = {500}, tau derived from autocorelation (tau = x s.t. y[x]=y[0]*exp(-1)) = {tau}')
	print(f'True wn mean = {wn_mean}, measured wn mean = {gm_500_wn_mean}')
	print(f'True wn std = {wn_std}, measured wn std = {gm_500_wn_std}')

	plt.show()


if __name__ == '__main__':
	main()

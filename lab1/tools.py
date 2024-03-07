import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from allan_variance import allan_variance


def white_noise(n_series, length, mean=0, std=1, random_seed=42):
	np.random.seed(random_seed)
	wn = mean + std * np.random.randn(n_series, length)
	return wn


def random_walk(wn):
	return np.cumsum(wn, axis=1)


def gauss_markov(wn, tau, dt=1):
	length = wn.shape[1]
	beta = 1 / tau
	gm = np.zeros_like(wn)  # Assume gm[0] = 0
	for i in range(1, length):
		gm[:, i] = gm[:, i - 1] * np.exp(-beta * dt) + wn[:, i - 1]
	return gm


def autocorr_norm(x):
	ac = np.correlate(x, x, mode='full')
	ac_norm = (ac - np.min(ac)) / (np.max(ac) - np.min(ac))
	return ac_norm


def psd(x, dt=1):
	return signal.welch(x, fs=dt, return_onesided=False, scaling='spectrum')


def allan_var(x, dt=1):
	tau, av = allan_variance(x, dt, input_type='increment')
	return tau, av


# Plots functions

def create_subfigs(title, shape):
	fig = plt.figure(constrained_layout=True, figsize=(10, 10))
	subfigs = fig.subfigures(shape[0], shape[1], hspace=0.1)
	axs = []
	for i, subfig in enumerate(subfigs):
		axs.append(subfigs[i].subplots(1, 1))
	fig.suptitle(title)
	return fig, axs


def plot_1(ax, serie, title, legend, linewidth=1):
	ax.plot(serie.T, linewidth=linewidth)
	ax.title.set_text(title)
	leg = ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=3)

	# Correct line width in legend
	if linewidth != 1:
		lines_0 = leg.get_lines()
		for line in lines_0:
			line.set_linewidth(2)
	return leg


def plot_ac(ax, x, serie, title, legend):
	n_series = len(serie)
	for i in range(n_series):
		ax.plot(x, serie[i])
	ax.set_title(title)
	ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=3)


def plot_psd(ax, psd, title, legend):
	n_psd = len(psd)
	for i in range(n_psd):
		f1, S1 = psd[i]
		ax.plot(f1, S1)
	ax.set_title(title)
	ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=3)


def plot_loglog_av(ax, tau, av, title, legend):
	ax.loglog(tau, av)
	ax.set_title(title)
	ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.25))


def save_fig(fig, name, folder):
	fig.savefig(folder + "svg/" + name + '.svg', format='svg')
	fig.savefig(folder + "png/" + name + '.png', format='png')
# fig.savefig(folder + "eps/" + name + '.eps', format='eps')

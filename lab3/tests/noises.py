import os

from lab3.src.noise import NoiseModel as NsM

if __name__ == '__main__':

    folder = '../../data/noises/'
    if not os.path.exists(folder):
        os.mkdir(path=folder)

    size = 200
    NsM.Bias(bias_sd=1).plot_noise(size=size, n_serie=2, path=folder + 'bias.jpg')
    NsM.WhiteNoise(psd_wn=1).plot_noise(size=size, n_serie=2, path=folder + 'WN.jpg')
    NsM.RandomWalk(psd_wn=1).plot_noise(size=size, n_serie=2, path=folder + 'RW.jpg')
    NsM.GaussMarkov(psd_gm=1, tau=1).plot_noise(size=size, n_serie=2, path=folder + 'GM.jpg')

import numpy as np
import pylab as p


class KalmanFilter:
    """

    Assume constant phi,g,q,r
    """
    def __init__(self, x0, p0, phi, q, h):

        self.x_est = x0
        self.p_est = p0
        self.phi = phi
        self.q = q
        self.h = h

        self.k = None
        self.x_pred = None
        self.p_pred = None

    def predict(self):
        x_est, p_est, phi, q = self.x_est, self.p_est, self.phi, self.q

        self.x_pred = phi @ x_est
        self.p_pred = phi @ p_est @ phi.T + q

    def add_measure(self, z, r):
        self.gain(r)
        self.state_update(z)
        self.covar_update()

    def gain(self, r):
        p_pred, h, r = self.p_pred, self.h, self.r
        self.k = np.linalg.solve(h @ p_pred @ h.T + r, p_pred @ h.t)

    def state_update(self, z):
        x_pred, k, h = self.x_pred, self.k, self.h
        self.x_est = x_pred + k @ (z - h @ x_pred)

    def covar_update(self):
        k, h, p_pred = self.k, self.h, self.p_pred
        i = np.identity(p_pred.shape)
        self.p_est = (i - k @ h) @ p_pred

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
        p_pred, h = self.p_pred, self.h
        # self.k = p_pred @ h.T @ np.linalg.inv(h @ p_pred @ h.T + r)
        A = (h @ p_pred @ h.T + r).T
        b = (p_pred @ h.T).T
        pass
        self.k = np.linalg.solve(A, b).T

    def state_update(self, z):
        x_pred, k, h = self.x_pred, self.k, self.h
        self.x_est = x_pred + k @ (z - h @ x_pred)

    def covar_update(self):
        k, h, p_pred = self.k, self.h, self.p_pred
        i = np.eye(p_pred.shape[0])
        self.p_est = (i - k @ h) @ p_pred

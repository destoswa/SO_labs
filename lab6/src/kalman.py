import numpy as np
import pylab as p


class KalmanFilter:
    """

    Assume constant phi,g,q,r
    """

    def __init__(self, x0, p0, phi, q, h, r):
        self.dx_est = x0
        self.p_est = p0
        self.phi = phi
        self.q = q
        self.h = h
        self.r = r

        self.k = None
        self.dx_pred = None
        self.p_pred = None

    def predict(self):
        dx_est, p_est, phi, q = self.x_est, self.p_est, self.phi, self.q
        self.dx_pred = phi @ dx_est
        self.p_pred = phi @ p_est @ phi.T + q

    def no_meas_update(self):
        self.dx_est = self.dx_pred
        self.p_est = self.p_pred

    def update(self, z):
        self.gain()
        self.state_update(z)
        self.covar_update()

    def gain(self):
        p_pred, h, r = self.p_pred, self.h, self.r
        # self.k = p_est @ h.T @ np.linalg.inv(h @ p_est @ h.T + r)
        A = (h @ p_pred @ h.T + r).T
        b = (p_pred @ h.T).T
        self.k = np.linalg.solve(A, b).T

    def state_update(self, z):
        dx_pred, k, h = self.dx_pred, self.k, self.h

        # === RESCALE MANUEL POUR TESTS ===
        #k[:2,:] = k[:2,:] * 0.5
        #k[2:,:] = k[2:,:] * 0.3
        # =================================

        self.x_est = dx_pred + k @ (z - h @ dx_pred)

    def covar_update(self):
        k, h, p_pred = self.k, self.h, self.p_pred
        i = np.eye(p_pred.shape[0])
        self.p_est = (i - k @ h) @ p_pred

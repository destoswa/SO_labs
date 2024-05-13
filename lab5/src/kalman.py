import numpy as np
import pylab as p


class KalmanFilter:
    """

    Assume constant phi,g,q,r
    """

    def __init__(self, x0, p0, phi, q, h, r):
        self.x_est = x0
        self.p_est = p0
        self.phi = phi
        self.q = q
        self.h = h
        self.r = r

        self.k = None
        #self.x_pred = None
        #self.p_pred = None

    def predict(self):
        x_est, p_est, phi, q = self.x_est, self.p_est, self.phi, self.q

        self.x_est = phi @ x_est
        self.p_est = phi @ p_est @ phi.T + q

    def update(self, z):
        self.gain()
        self.state_update(z)
        self.covar_update()

    def gain(self):
        p_est, h, r = self.p_est, self.h, self.r
        #self.k = p_est @ h.T @ np.linalg.inv(h @ p_est @ h.T + r)
        A = (h @ p_est @ h.T + r).T
        b = (p_est @ h.T).T
        self.k = np.linalg.solve(A, b).T

    def state_update(self, z):
        x_est, k, h = self.x_est, self.k, self.h

        # === RESCALE MANUEL POUR TESTS ===
        #k[:2,:] = k[:2,:] * 0.5
        #k[2:,:] = k[2:,:] * 0.3
        # =================================

        self.x_est = x_est + k @ (z - h @ x_est)

    def covar_update(self):
        k, h, p_est = self.k, self.h, self.p_est
        i = np.eye(p_est.shape[0])
        self.p_est = (i - k @ h) @ p_est


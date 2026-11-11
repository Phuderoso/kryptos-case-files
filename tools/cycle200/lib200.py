"""Cycle 200 — serial-dependence ("rhythm") panel for K4 (IDEAS I-233b / I-236).

Panel on a letter string x (length n), lags d = 1..48 measured on the contiguous carved text
(no positions are excised, so the nominal lag is the true pair distance; Voynich C104 lesson):
  A(d)     = #{i : x_i == x_{i+d}}                        (kappa / coincidence at lag d)
  BAZ(d)   = sum_v C(m_v, 2), m_v = #{i : (x_{i+d}-x_i) mod 26 == v}, A-Z numbering
  BKA(d)   = same with KRYPTOS-alphabet numbering
  SA(L)    = A(1) + ... + A(L), L = 2..16                 (short-lag window: 'one alphabet per column')
All statistics are 'more structure = larger'. 48 + 48 + 48 + 15 = 159 statistics.
"""
import numpy as np

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
assert len(K4) == 97
DMAX = 48
LWIN = list(range(2, 17))
KAPOS = np.array([KA.index(c) for c in AZ])  # AZ index -> KA index


PER = list(range(4, 27))   # PHI periods 4..26
PERB = list(range(4, 17))  # difference-repeat lags 4..16


def names():
    """Registered panel (64 statistics): PHI(p), p 4..26 = sum_k A(kp), kp <= 48 (period kappa, alphabet-agnostic);
    BAZ(p), BKA(p), p 4..16 (difference repeats, progressive keys); SA(L) (short-lag window)."""
    return ([f"PHI{p}" for p in PER] + [f"BAZ{p}" for p in PERB] + [f"BKA{p}" for p in PERB]
            + [f"SA{L}" for L in LWIN])


def panel(X):
    F = full_panel(X)
    A = F[:, :DMAX]
    phi = [A[:, [k * p - 1 for k in range(1, DMAX // p + 1)]].sum(1) for p in PER]
    baz = [F[:, DMAX + p - 1] for p in PERB]
    bka = [F[:, 2 * DMAX + p - 1] for p in PERB]
    return np.concatenate([np.stack(phi + baz + bka, 1), F[:, 3 * DMAX:]], 1)


def full_names():
    return ([f"A{d}" for d in range(1, DMAX + 1)] + [f"BAZ{d}" for d in range(1, DMAX + 1)]
            + [f"BKA{d}" for d in range(1, DMAX + 1)] + [f"SA{L}" for L in LWIN])


def enc(s):
    return np.array([AZ.index(c) for c in s], dtype=np.int64)


def _diffrep(Y, d):
    N, n = Y.shape
    delta = (Y[:, d:] - Y[:, :-d]) % 26
    idx = delta + 26 * np.arange(N)[:, None]
    m = np.bincount(idx.ravel(), minlength=26 * N).reshape(N, 26)
    return (m * (m - 1) // 2).sum(1)


def full_panel(X):
    """X: (N, n) int array of A-Z indices. Returns (N, 159) int array."""
    X = np.atleast_2d(X)
    Y = KAPOS[X]
    cols = []
    A = [(X[:, :-d] == X[:, d:]).sum(1) for d in range(1, DMAX + 1)]
    cols += A
    cols += [_diffrep(X, d) for d in range(1, DMAX + 1)]
    cols += [_diffrep(Y, d) for d in range(1, DMAX + 1)]
    cA = np.cumsum(np.stack(A, 1), 1)
    cols += [cA[:, L - 1] for L in LWIN]
    return np.stack(cols, 1)


def shuffles(x, N, seed):
    rng = np.random.default_rng(seed)
    X = np.tile(x, (N, 1))
    return rng.permuted(X, axis=1)


class Meter:
    """z-scores from a calibration null (N0) and a held-out null (N1) for the max/min statistics."""

    def __init__(self, x, n0, s0, n1, s1):
        P0 = panel(shuffles(x, n0, s0)).astype(float)
        self.mu = P0.mean(0)
        self.sd = P0.std(0, ddof=1)
        self.sd[self.sd == 0] = 1.0
        P1 = self.z(panel(shuffles(x, n1, s1)))
        self.zmax1 = np.sort(P1.max(1))
        self.zmin1 = np.sort(P1.min(1))

    def z(self, P):
        return (np.atleast_2d(P) - self.mu) / self.sd

    def crit_hi(self, alpha):
        return float(np.quantile(self.zmax1, 1 - alpha))

    def crit_lo(self, alpha):
        return float(np.quantile(self.zmin1, alpha))

    def p_hi(self, zmax):
        return (1 + np.sum(self.zmax1 >= zmax)) / (1 + len(self.zmax1))

    def p_lo(self, zmin):
        return (1 + np.sum(self.zmin1 <= zmin)) / (1 + len(self.zmin1))

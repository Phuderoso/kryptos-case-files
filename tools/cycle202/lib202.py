"""Cycle 202 — confirmatory COL_P reverse test at the 8 SAT-open periods under C3 (IDEAS I-245).

Re-uses cycle 201's plant machinery unchanged (lib201: H_P plants, C3 = crib-consistent alphabets + forced letters + bans
with a unigram repair).  Adds:
  * plant_c3b: the same C3 plant, but a banned letter is repaired from a bigram (both neighbours) law of the model,
    restricted to allowed letters (sensitivity check for I-246; descriptive only).
  * mc_q: Monte-Carlo reverse q = (1 + #{plant z <= z_K4}) / (n + 1) (ties count against disfavouring).
  * holm: Holm step-down over the 8 periods.
H_P = one bijection per phase i mod P, applied directly; COL_P = sum over phases of sum_letters C(n, 2).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle201"))
import lib201 as L  # noqa: E402

AZ, K4, N, CRIBPOS = L.AZ, L.K4, L.N, L.CRIBPOS
OPEN = [8, 13, 16, 19, 20, 23, 24, 26]
MODELS = ["JE", "CARTER", "K123", "JEX"]


def bigram(txt):
    x = L.enc(txt[:400000])
    B = np.ones((26, 26))
    np.add.at(B, (x[:-1], x[1:]), 1)
    return B


def plant_c3b(rng, txt, P, B, U):
    """C3 plant with a bigram repair: banned letter at j drawn with weight P(c | prev) * P(next | c) over allowed c (first-order chain)
    (left to right, so a repaired left neighbour is used).  Forced letters and cribs as in C3."""
    pt = list(L.with_cribs(L.window(rng, txt)))
    for j, c in L.forced_positions(P).items():
        pt[j] = c
    for j, bad in sorted(L.forbidden(P).items()):
        if AZ.index(pt[j]) in bad:
            w = np.ones(26)
            if j > 0:
                w *= B[AZ.index(pt[j - 1]), :] / B[AZ.index(pt[j - 1]), :].sum()
            if j < N - 1:
                w *= B[:, AZ.index(pt[j + 1])] / B.sum(1)
            w[list(bad)] = 0; w /= w.sum()
            pt[j] = AZ[int(rng.choice(26, p=w))]
    x = L.enc("".join(pt))
    al = L.alphabets(rng, P, 3)
    y = np.array([al[i % P][x[i]] for i in range(N)])
    return x, y


def mc_q(zs, z0):
    zs = np.asarray(zs)
    return float((1 + np.sum(zs <= z0)) / (len(zs) + 1))


def holm(qs, alpha=0.05):
    """qs: dict period -> q. Returns dict period -> (rejected, threshold used)."""
    order = sorted(qs, key=qs.get)
    m = len(order); out = {}; stop = False
    for i, p in enumerate(order):
        thr = alpha / (m - i)
        rej = (not stop) and qs[p] <= thr
        if not rej:
            stop = True
        out[p] = (bool(rej), thr)
    return out

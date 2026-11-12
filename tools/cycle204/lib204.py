"""Cycle 204 — exact conditioning of the COL_P reverse test (IDEAS I-252, with I-254 / I-260).

Case 189 (cycle 202) put P 8 at STAT-DISFAVOURED (repair-sensitive): its C3 plants are real text windows with the cribs and
crib-forced letters written in and each *banned* letter (one the per-phase bijection would send onto a crib-position K4 letter where
K4 has another letter) repaired by a unigram draw.  Real windows cannot be rejection-sampled under ~200 bans + 29 fixed letters.

This cycle samples the plaintext EXACTLY from the conditional law of an order-k character Markov chain (k = 3: quadgram chain,
k = 4 sensitivity) given every C3 constraint as a hard per-position mask (cribs and forced letters = singletons, bans = complement),
by forward filtering / backward sampling (FFBS).  No repair step exists, so the repair sensitivity is removed *within the chain*.
The chain's fidelity to real text for COL_P is a gate (G6), measured by running case 189's C3 repair recipe on chain samples and on
real windows.

z values use the exact permutation moments of COL_P (formula of the Voynich desk's I-254 audit, re-implemented and re-checked here):
  p2 = sum m(m-1)/(n)_2, p3 = sum m(m-1)(m-2)/(n)_3, p22 = [sum m(m-1)(m-2)(m-3) + (sum m(m-1))^2 - sum (m(m-1))^2]/(n)_4
  E = |E| p2, Var = |E|(p2-p2^2) + S(p3-p2^2) + D(p22-p2^2), |E| = sum_f C(s_f,2), S = sum_f s_f(s_f-1)(s_f-2), D = |E|(|E|-1)-S.
"""
import os, sys, re
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle201"))
import lib201 as L  # noqa: E402

AZ, K4, N, CRIBPOS = L.AZ, L.K4, L.N, L.CRIBPOS
K4X = L.enc(K4)
OPEN = [8, 13, 16, 19, 20, 23, 24, 26]
REG_MODELS = ["JE", "CARTER", "K123MIX", "JEX"]
DESC_MODELS = ["DRAC"]


# ---------------- exact moments of COL_P ----------------
def col_moments(counts, P, n=N):
    """counts: (R, 26) letter counts of R texts of length n.  Returns (mean, sd) arrays of COL_P under a uniform permutation."""
    m = np.atleast_2d(np.asarray(counts, dtype=float))
    def ff(k):
        return float(np.prod([n - t for t in range(k)]))
    s2 = m * (m - 1)
    p2 = s2.sum(1) / ff(2)
    p3 = (s2 * (m - 2)).sum(1) / ff(3)
    p22 = ((s2 * (m - 2) * (m - 3)).sum(1) + s2.sum(1) ** 2 - (s2 ** 2).sum(1)) / ff(4)
    s = np.array([len(range(f, n, P)) for f in range(P)], dtype=float)
    E = (s * (s - 1) / 2).sum(); S = (s * (s - 1) * (s - 2)).sum(); D = E * (E - 1) - S
    mu = E * p2
    var = E * (p2 - p2 ** 2) + S * (p3 - p2 ** 2) + D * (p22 - p2 ** 2)
    return mu, np.sqrt(np.maximum(var, 1e-300))


def counts(X):
    X = np.atleast_2d(X); R = X.shape[0]
    return np.bincount((X + 26 * np.arange(R)[:, None]).ravel(), minlength=26 * R).reshape(R, 26)


def z_exact(X, P):
    """exact-moment z of COL_P of each row of X (against permutations of the row's own multiset)."""
    mu, sd = col_moments(counts(X), P, X.shape[-1])
    return (L.col(X, P) - mu) / sd


# ---------------- plaintext models ----------------
def load(sup):
    T = L.load_models(sup)
    d = open(f"{sup}/pg345.txt", encoding="utf-8", errors="ignore").read()
    i, j = d.find("CHAPTER I"), d.find("*** END OF")
    T["DRAC"] = L._letters(d[i:j])
    return T


def ngram_counts(x, k):
    """counts of (k+1)-grams of the index array x, shape (26,)*(k+1)."""
    idx = np.zeros(len(x) - k, dtype=np.int64)
    for t in range(k + 1):
        idx = idx * 26 + x[t:len(x) - k + t]
    return np.bincount(idx, minlength=26 ** (k + 1)).reshape((26,) * (k + 1)).astype(float)


def chain(txts_weights, k, beta=1.0):
    """Order-k chain with recursive Dirichlet back-off: P_j(d|ctx) = (C(ctx d) + beta P_{j-1}(d|ctx'))/(C(ctx) + beta).
    txts_weights: list of (text, weight); counts are summed with the weights (K123MIX = K1-K3 scaled to Jane Eyre's mass + JE).
    Returns (T, init): T[(26,)*k + (26,)] transition, init[(26,)*k] start law (smoothed k-gram frequency)."""
    xs = [(L.enc(t), w) for t, w in txts_weights]
    uni = sum(w * np.bincount(x, minlength=26) for x, w in xs) + 1.0
    Pj = uni / uni.sum()                                   # order 0
    for j in range(1, k + 1):
        C = sum(w * ngram_counts(x, j) for x, w in xs)     # (26,)*(j+1)
        ctx = C.sum(-1, keepdims=True)
        back = Pj.reshape((1,) + Pj.shape) if j > 1 else Pj.reshape((1,) * j + (26,))
        Pj = (C + beta * np.broadcast_to(back, C.shape)) / (ctx + beta)
    T = Pj
    G = sum(w * ngram_counts(x, k - 1) for x, w in xs) + 0.01
    init = G / G.sum()
    return T, init


def model_chain(T_txt, name, k):
    if name == "K123MIX":
        je, kk = T_txt["JE"], T_txt["K123"]
        return chain([(je, 1.0), (kk, len(je) / len(kk))], k)
    return chain([(T_txt[name], 1.0)], k)


# ---------------- C3 masks ----------------
def mask(P, cond=3):
    """(N, 26) bool allowed letters: cribs, crib-forced letters (C2), bans (C3).  cond 0 = no constraint."""
    M = np.ones((N, 26), dtype=bool)
    if cond == 0:
        return M
    for p, c in CRIBPOS.items():
        M[p] = False; M[p, AZ.index(c)] = True
    for j, c in L.forced_positions(P).items():
        M[j] = False; M[j, AZ.index(c)] = True
    for j, bad in L.forbidden(P).items():
        M[j, list(bad)] = False
    return M


# ---------------- FFBS ----------------
def ffbs(rng, T, init, M, n):
    """n exact samples of x_0..x_{N-1} from the order-k chain conditioned on x_i in M[i] for all i."""
    k = init.ndim
    a = init.copy()
    for t in range(k):
        sh = [1] * k; sh[t] = 26
        a = a * M[t].reshape(sh)
    a /= a.sum()
    alphas = [a]
    letters = "abcdefghij"[:k + 1]
    sub = f"{letters[:k]},{letters}->{letters[1:]}"
    for i in range(k, N):
        a = np.einsum(sub, a, T) * M[i].reshape((1,) * (k - 1) + (26,))
        s = a.sum()
        if s <= 0:
            raise ValueError("empty conditional law")
        a = a / s
        alphas.append(a)
    X = np.zeros((n, N), dtype=np.int64)
    flat = alphas[-1].ravel()
    st = rng.choice(flat.size, size=n, p=flat / flat.sum())
    tail = np.array(np.unravel_index(st, (26,) * k)).T      # (n, k): x_{N-k} .. x_{N-1}
    X[:, N - k:] = tail
    for i in range(N - k - 1, -1, -1):
        # state at position i+k-1 (alphas index i) = (x_i .. x_{i+k-1}); next letter x_{i+k}
        A = alphas[i]                                          # shape (26,)*k over (x_i .. x_{i+k-1})
        rest = tuple(X[:, i + 1 + t] for t in range(k - 1))    # x_{i+1} .. x_{i+k-1}
        w = A[(slice(None),) + rest] if k > 1 else np.broadcast_to(A, (n, 26)).T
        w = w.T if k > 1 else w.T                              # (n, 26) over x_i
        tr = T[(slice(None),) + rest + (X[:, i + k],)].T if k > 1 else T[:, X[:, i + k]].T
        w = w * tr
        w = w / w.sum(1, keepdims=True)
        u = rng.random(n)[:, None]
        X[:, i] = (np.cumsum(w, 1) < u).sum(1).clip(0, 25)
    return X


def forward_sample(rng, T, init, n):
    """unconstrained chain samples (for the chain-C3 repair recipe and G5)."""
    k = init.ndim
    X = np.zeros((n, N), dtype=np.int64)
    flat = init.ravel()
    st = rng.choice(flat.size, size=n, p=flat)
    X[:, :k] = np.array(np.unravel_index(st, (26,) * k)).T
    for i in range(k, N):
        w = T[tuple(X[:, i - k + t] for t in range(k))]
        u = rng.random(n)[:, None]
        X[:, i] = (np.cumsum(w, 1) < u).sum(1).clip(0, 25)
    return X


# ---------------- C3 repair recipe (case 189, vectorised) and ciphertexts ----------------
def windows(rng, txt, n):
    x = L.enc(txt)
    o = rng.integers(0, len(x) - N + 1, size=n)
    return x[o[:, None] + np.arange(N)[None, :]]


def c3_repair(rng, X, P, uni):
    """cribs + forced letters written in; banned letters redrawn from the unigram law restricted to allowed letters."""
    X = X.copy()
    for p, c in CRIBPOS.items():
        X[:, p] = AZ.index(c)
    for j, c in L.forced_positions(P).items():
        X[:, j] = AZ.index(c)
    for j, bad in L.forbidden(P).items():
        badl = list(bad)
        hit = np.isin(X[:, j], badl)
        if hit.any():
            w = uni.copy(); w[badl] = 0; w /= w.sum()
            X[hit, j] = rng.choice(26, size=int(hit.sum()), p=w)
    return X


def encipher(rng, X, P):
    """per-phase bijections agreeing with K4's crib pairs (lib201.alphabets(cond=3)), vectorised over rows."""
    n = X.shape[0]
    fw = L.crib_maps(P)
    A = np.zeros((n, P, 26), dtype=np.int64)
    for f in range(P):
        a = np.full(26, -1)
        for kk, v in fw[f].items():
            a[kk] = v
        free_pt = [kk for kk in range(26) if a[kk] < 0]
        free_ct = np.array([v for v in range(26) if v not in fw[f].values()])
        A[:, f, :] = a
        perm = np.argsort(rng.random((n, len(free_pt))), axis=1)
        A[:, f, free_pt] = free_ct[perm]
    ph = np.arange(N) % P
    return A[np.arange(n)[:, None], ph[None, :], X]


def consistent_rows(Y, P):
    K = K4X
    ok = np.ones(Y.shape[0], dtype=bool)
    for p in CRIBPOS:
        ok &= Y[:, p] == K[p]
    for j in L.forced_positions(P):
        ok &= Y[:, j] == K[j]
    img = [set(m.values()) for m in L.crib_maps(P)]
    for j in L.forbidden(P):
        ok &= ~np.isin(Y[:, j], list(img[j % P]))
    return ok


def mc_q(zs, z0):
    zs = np.asarray(zs)
    return float((1 + np.sum(zs <= z0)) / (len(zs) + 1))


def holm(qs, alpha=0.05):
    order = sorted(qs, key=qs.get)
    m = len(order); out = {}; stop = False
    for i, p in enumerate(order):
        thr = alpha / (m - i)
        rej = (not stop) and qs[p] <= thr
        if not rej:
            stop = True
        out[p] = (bool(rej), thr)
    return out

"""Cycle 201 — robustness of case 187's STAT-DISFAVOURED cells (IDEAS I-238).

H_P = periodic substitution, P arbitrary alphabets (one bijection per phase i mod P), applied directly to the
97-letter plaintext (no transposition).  Statistics (lags on the contiguous text, nominal lag = true distance):
  PHI_P = sum_k A(kP), kP <= 48   (registered in case 187; A(d) = #{i : x_i == x_{i+d}})
  COL_P = sum over phases of sum_letters C(n, 2)   (all same-phase pairs; Friedman column IC; secondary here)
Invariance (gate G1): under H_P both statistics of the ciphertext equal those of the plaintext, because same-phase
pairs share one bijection.  So the alphabets only move the shuffle null (via the ciphertext letter frequencies).
"""
import re
import numpy as np

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
assert len(K4) == 97
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}   # 0-indexed starts (1-indexed 22-34, 64-74)
CRIBPOS = {st + k: w[k] for st, w in CRIBS.items() for k in range(len(w))}
DMAX = 48
N = 97


def enc(s):
    return np.array([AZ.index(c) for c in s], dtype=np.int64)


def phi(X, P):
    X = np.atleast_2d(X)
    return sum((X[:, :-d] == X[:, d:]).sum(1) for d in range(P, DMAX + 1, P))


def col(X, P):
    X = np.atleast_2d(X)
    R = X.shape[0]
    tot = np.zeros(R, dtype=np.int64)
    for f in range(P):
        Y = X[:, f::P]
        m = np.bincount((Y + 26 * np.arange(R)[:, None]).ravel(), minlength=26 * R).reshape(R, 26)
        tot += (m * (m - 1) // 2).sum(1)
    return tot


def shuffles(x, n, seed):
    rng = np.random.default_rng(seed)
    return rng.permuted(np.tile(x, (n, 1)), axis=1)


def own_z(x, P, n, seed):
    """z of PHI_P and COL_P of x against n shuffles of x itself (case 187's own-text null)."""
    S = shuffles(x, n, seed)
    out = []
    for f in (phi, col):
        v = f(S, P).astype(float); mu, sd = v.mean(), v.std(ddof=1)
        out.append((float(f(x, P)[0]) - mu) / (sd if sd > 0 else 1.0))
    return out


# ---------------- plaintext models ----------------
def _letters(t):
    return re.sub("[^A-Z]", "", t.upper())


def load_models(sup):
    je_raw = open(f"{sup}/rk_plain.txt", encoding="utf-8", errors="ignore").read()
    i, j = je_raw.find("CHAPTER I"), je_raw.find("*** END OF")
    je_raw = je_raw[i:j]
    car = open(f"{sup}/carter1.txt", encoding="utf-8", errors="ignore").read()
    e = open(f"{sup}/k123_eng.txt").read().strip()
    k1 = "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION"
    k2 = e[e.find("ITWASTOTALLY"):e.find("IDBYROWS") + 8]
    k3 = e[e.find("SLOWLY"):]
    return {
        "JE": _letters(je_raw),                                   # Jane Eyre (case 187's model)
        "CARTER": _letters(car[25000:]),                          # Carter & Mace 1923 vol. I, IA OCR (K3's source), after the contents
        "K123": k1 + k2 + k3,                                     # Sanborn's own K1-K3 plaintexts (as carved, misspellings kept)
        "JEX": _letters(re.sub(r"[.!?;:]", " X ", je_raw)),       # Jane Eyre with an X at every sentence / clause stop (K2 style)
    }


def window(rng, txt, n=N):
    o = int(rng.integers(0, len(txt) - n + 1))
    return txt[o:o + n]


def with_cribs(pt):
    s = list(pt)
    for p, c in CRIBPOS.items():
        s[p] = c
    return "".join(s)


def crib_maps(P):
    """Per phase: forced pt->ct pairs from K4's crib letters (consistent at the SAT-open periods)."""
    fw = [dict() for _ in range(P)]
    for p, c in CRIBPOS.items():
        f = p % P
        a, b = AZ.index(c), AZ.index(K4[p])
        if fw[f].get(a, b) != b or b in [v for k, v in fw[f].items() if k != a]:
            raise ValueError(f"crib-inconsistent at P={P} phase {f}")
        fw[f][a] = b
    return fw


def forced_positions(P):
    """C2: non-crib positions j whose K4 letter equals a crib-position K4 letter of the same phase -> pt_j forced."""
    fw = crib_maps(P)
    inv = [{b: a for a, b in m.items()} for m in fw]
    out = {}
    for j in range(N):
        if j in CRIBPOS:
            continue
        b = AZ.index(K4[j])
        if b in inv[j % P]:
            out[j] = AZ[inv[j % P][b]]
    return out


def forbidden(P):
    """C3: non-crib, non-forced positions j: K4[j] is not one of the crib-position K4 letters of its phase, so under
    H_P its plaintext letter cannot be one of that phase's crib plaintext letters (bijection)."""
    fw = crib_maps(P)
    fp = forced_positions(P)
    out = {}
    for j in range(N):
        if j in CRIBPOS or j in fp:
            continue
        dom = set(fw[j % P].keys())
        if dom:
            out[j] = dom
    return out


def unigram(txt):
    c = np.bincount(enc(txt[:200000]), minlength=26).astype(float)
    return c / c.sum()


def alphabets(rng, P, cond):
    al = []
    fw = crib_maps(P) if cond >= 1 else [dict() for _ in range(P)]
    for f in range(P):
        a = np.full(26, -1)
        for k, v in fw[f].items():
            a[k] = v
        free_pt = [k for k in range(26) if a[k] < 0]
        free_ct = [v for v in range(26) if v not in fw[f].values()]
        a[free_pt] = rng.permutation(free_ct)
        al.append(a)
    return al


def plant(rng, txt, P, cond, dilute=0.0, uni=None):
    """One H_P plant: (plaintext indices, ciphertext indices). cond 0 = case 187 recipe, 1 = crib-consistent
    alphabets, 2 = 1 + plaintext letters forced by K4's same-phase repeats of crib-position letters,
    3 = 2 + the negative constraint (forbidden(P)): a letter that the bijection would send to a crib-position K4
    letter where K4 has another letter is repaired by a draw from the model's unigram law restricted to allowed letters.
    Under C3 every same-phase relation between a crib position and any other position matches K4 exactly."""
    pt = list(with_cribs(window(rng, txt)))
    if dilute > 0:
        for j in range(N):
            if j not in CRIBPOS and rng.random() < dilute:
                pt[j] = AZ[int(rng.integers(0, 26))]
    if cond >= 2:
        for j, c in forced_positions(P).items():
            pt[j] = c
    if cond >= 3:
        for j, bad in forbidden(P).items():
            if AZ.index(pt[j]) in bad:
                w = uni.copy(); w[list(bad)] = 0; w /= w.sum()
                pt[j] = AZ[int(rng.choice(26, p=w))]
    x = enc("".join(pt))
    al = alphabets(rng, P, cond)
    y = np.array([al[i % P][x[i]] for i in range(N)])
    return x, y


def consistent(y, P, cond):
    """Gate G1b: the plant ciphertext agrees with K4 wherever the conditioning level says it must."""
    K = enc(K4)
    if cond >= 1 and any(y[p] != K[p] for p in CRIBPOS):
        return False
    if cond >= 2 and any(y[j] != K[j] for j in forced_positions(P)):
        return False
    if cond >= 3:
        img = [set(m.values()) for m in crib_maps(P)]
        if any(y[j] in img[j % P] for j in forbidden(P)):
            return False
    return True

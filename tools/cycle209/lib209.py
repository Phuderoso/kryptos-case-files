"""Cycle 209 (IDEAS I-247): Quagmire IV conditioning of the COL_P reverse test at the SAT-open periods.

Case 188 / 191 condition the plaintext on C3, the exact single-position marginal of the crib constraints under H_P (one free bijection
per phase).  Quagmire IV (case 11's F1: CA^-1(c_i) = PA^-1(p_i) + k_{i mod P}, PA, CA arbitrary) is a sub-family of H_P that ties the
phases together, so its single-position marginal C4 can only ban more.  C4[x] = {p : some (PA, CA, k) consistent with the 24 crib pairs
also maps p -> K4[x] at phase x mod P}.  Decided exactly by CP-SAT on the reduced model (only the letters that touch the cribs or the
query get variables; exact because any injective partial map extends to a full alphabet; rotation fixed by f[first pt letter] = 0).
UNKNOWN (time limit) is counted and treated as allowed, which keeps the mask a superset of exact C4 (conservative toward C3)."""
import sys, os
import numpy as np
from ortools.sat.python import cp_model
_H = os.path.dirname(os.path.abspath(__file__))
for _d in ("cycle201", "cycle204"):
    for _b in (os.path.join(_H, ".."), "/tmp/kcf/tools"):
        if os.path.isdir(os.path.join(_b, _d)): sys.path.insert(0, os.path.join(_b, _d)); break
import lib201 as L
AZ, N = L.AZ, L.N


def crib_pairs(ct, cribpos=None):
    cribpos = L.CRIBPOS if cribpos is None else cribpos
    return [(pos, AZ.index(ch), AZ.index(ct[pos])) for pos, ch in sorted(cribpos.items())]


def qiv_model(P, pairs):
    ptl = sorted({p for _, p, _ in pairs}); ctl = sorted({c for _, _, c in pairs})
    m = cp_model.CpModel()
    f = {a: m.NewIntVar(0, 25, f"f{a}") for a in ptl}; g = {a: m.NewIntVar(0, 25, f"g{a}") for a in ctl}
    k = [m.NewIntVar(0, 25, f"k{i}") for i in range(P)]
    m.AddAllDifferent(list(f.values())); m.AddAllDifferent(list(g.values()))
    m.Add(f[ptl[0]] == 0)
    for pos, p, c in pairs:
        b = m.NewIntVar(0, 1, ""); m.Add(g[c] == f[p] + k[pos % P] - 26 * b)
    return m, f, g, k


def qiv_status(P, pairs, workers=1, tl=20.0, seed=0):
    m, f, g, k = qiv_model(P, pairs)
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tl
    s.parameters.random_seed = seed
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return "SAT", ({a: s.Value(v) for a, v in f.items()}, {a: s.Value(v) for a, v in g.items()}, [s.Value(v) for v in k])
    return ("UNSAT" if st == cp_model.INFEASIBLE else "UNKNOWN"), None


def c3_mask_for(P, ct):
    """case 188 C3 (exact single-position marginal under H_P) for any ciphertext."""
    pairs = crib_pairs(ct); cribpos = {p for p, _, _ in pairs}
    fw = [dict() for _ in range(P)]
    for pos, p, c in pairs: fw[pos % P][p] = c
    M = np.ones((N, 26), dtype=bool)
    for pos, p, c in pairs: M[pos] = False; M[pos, p] = True
    for x in range(N):
        if x in cribpos: continue
        ph, c = x % P, AZ.index(ct[x]); inv = {v: kk for kk, v in fw[ph].items()}
        if c in inv: M[x] = False; M[x, inv[c]] = True
        else: M[x, list(fw[ph].keys())] = False
    return M


def _q(args):
    P, pairs, ph, p, c, tl = args
    st, _ = qiv_status(P, pairs + [(ph, p, c)], 1, tl)
    return (ph, p, c), st


def c4_mask(P, ct, procs=8, tl=20.0):
    from multiprocessing import Pool
    pairs = crib_pairs(ct); cribpos = {p for p, _, _ in pairs}
    M3 = c3_mask_for(P, ct)
    groups = {}
    for x in range(N):
        if x in cribpos: continue
        groups.setdefault((x % P, AZ.index(ct[x])), x)
    jobs = []
    for (ph, c), x in groups.items():
        cand = np.flatnonzero(M3[x]).tolist()
        if len(cand) == 1: continue                   # C3-forced: every H_P key (so every QIV key) maps it; checked by G-sound
        jobs += [(P, pairs, ph, p, c, tl) for p in cand]
    with Pool(procs) as pool:
        out = dict(pool.map(_q, jobs, chunksize=4))
    M = M3.copy(); unk = 0; extra = 0
    for x in range(N):
        if x in cribpos: continue
        key0 = (x % P, AZ.index(ct[x]))
        for p in np.flatnonzero(M3[x]):
            st = out.get((key0[0], int(p), key0[1]))
            if st is None: continue
            if st == "UNSAT": M[x, p] = False
            elif st == "UNKNOWN": unk += 1
    stats = dict(queries=len(jobs), unknown_query=sum(v == "UNKNOWN" for v in out.values()),
                 unsat_query=sum(v == "UNSAT" for v in out.values()), allowed_c3=int(M3.sum()), allowed_c4=int(M.sum()),
                 extra_bans_positions=int((M3 & ~M).sum()), empty_rows=int((M.sum(1) == 0).sum()))
    return M, stats


def qiv_plant(rng, x_txt, P):
    """English window with cribs written in, enciphered by a uniformly random Quagmire IV key of period P."""
    o = rng.integers(0, len(x_txt) - N); w = x_txt[o:o + N].copy()
    for p, c in L.CRIBPOS.items(): w[p] = AZ.index(c)
    PA = rng.permutation(26); CA = rng.permutation(26); k = rng.integers(0, 26, P)
    y = CA[(np.argsort(PA)[w] + k[np.arange(N) % P]) % 26]
    return w, "".join(AZ[i] for i in y)


def full_key_from_solution(rng, sol, P):
    """extend a reduced SAT solution (f on crib pt letters, g on crib ct letters, k) to full PA^-1, CA^-1 at random."""
    f, g, k = sol
    def extend(part):
        a = np.full(26, -1); used = set(part.values())
        for l, v in part.items(): a[l] = v
        free = [v for v in range(26) if v not in used]; rng.shuffle(free)
        a[a < 0] = free
        return a
    return extend(f), extend(g), np.array(k)


def qiv_encipher_rows(X, key, P):
    finv, ginv, k = key                     # finv = PA^-1 (letter -> index), ginv = CA^-1
    CA = np.argsort(ginv)
    return CA[(finv[X] + k[np.arange(N) % P][None, :]) % 26]

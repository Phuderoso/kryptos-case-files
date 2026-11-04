"""Cycle 7b: 'onion' preprocessing. Undo one simple monoalphabetic outer layer M before the layered test of
k4_layers.py (restricted transposition set): M in {Atbash(AZ), Atbash(KA), KA->AZ letter mapping, AZ->KA mapping,
Caesar shifts 1-25 on AZ and on KA}. CT' = M^-1(K4) is then tested exactly as in k4_layers.run."""
import sys
sys.path.insert(0, "tools")
import k4_layers as L
from k4_anneal import AZ, KA
K4 = L.K4
def mapping(src, dst): return lambda s: "".join(dst[src.index(c)] for c in s)
M = {"atbashAZ": mapping(AZ, AZ[::-1]), "atbashKA": mapping(KA, KA[::-1]), "KA->AZ": mapping(KA, AZ), "AZ->KA": mapping(AZ, KA)}
for k in range(1, 26):
    M[f"caesarAZ{k}"] = mapping(AZ, AZ[k:] + AZ[:k]); M[f"caesarKA{k}"] = mapping(KA, KA[k:] + KA[:k])
if __name__ == "__main__":
    from multiprocessing import Pool
    T = L.transpositions(full=False)
    with Pool() as pool:
        R = pool.starmap(L.run, [(f(K4), T, ("identity", "reverse", ("K3", 24, 8), ("K3", 8, 24)), {"KA": KA, "AZ": AZ}) for f in M.values()])
    tests = sum(r[0] for r in R); surv = [(n, x) for n, r in zip(M, R) for x in r[1]]
    best = sorted([(b[0], n) + b[1:] for n, r in zip(M, R) for b in r[2]], reverse=True)[:10]
    print(f"onion layers {len(M)}; transpositions {len(T)}; tests {tests:,}; full-crib survivors {len(surv)}")
    for s in surv: print("  SURVIVOR", s)
    print("best partial:"); [print("  ", b) for b in best]

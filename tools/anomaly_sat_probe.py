"""Budgeted parallel SAT over all anomaly patterns: python3 sat_probe2.py TEXT P1 P2 BUDGET (TEXT = K4 | null:SEED).
Reports per period: SAT / UNSAT / UNKNOWN (conflict budget exhausted) pattern counts and the SAT tags."""
import sys, time, random
from multiprocessing import Pool
from pysat.solvers import Cadical195
import anomaly_sat as S
from kryptos_text import K4
spec, P1, P2, BUD = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
if spec == "K4": CT = K4
else:
    l = list(K4); random.Random(int(spec[5:])).shuffle(l); CT = "".join(l)
pats = S.patterns()
class Grab:
    def __init__(self, bootstrap_with): self.cl = list(bootstrap_with); Grab.last = self.cl
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def solve(self): return None
def job(a):
    lst, tag, P = a; S.Cadical153 = Grab; S.model(CT, list(lst), P)
    with Cadical195(bootstrap_with=Grab.last) as s:
        s.conf_budget(BUD); r = s.solve_limited()
    return tag, r
if __name__ == "__main__":
    for P in range(P1, P2 + 1):
        with Pool(7) as pool: res = pool.map(job, [(l, t, P) for l, t in pats.items()], chunksize=1)
        sat = [t for t, r in res if r is True]; unk = [t for t, r in res if r is None]
        print(f"{spec} P={P}: SAT {len(sat)} UNSAT {len(res)-len(sat)-len(unk)} UNKNOWN {len(unk)} of {len(res)} | SAT {sat} | UNKNOWN {unk}", flush=True)

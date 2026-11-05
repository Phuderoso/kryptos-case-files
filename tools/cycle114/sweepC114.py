"""K4-only sweep of test C (generic V1 wheel, free alphabets) for n 8..20; sigma=-1 is redundant once both alphabets
are free (negate f, m and the shifts), so sigma=+1 only."""
import sys
from concurrent.futures import ProcessPoolExecutor
from sat114 import solve
from kryha114 import K4
def run(n): return n, solve(K4,n,1,timeout=90)
if __name__=="__main__":
    with ProcessPoolExecutor(3) as ex:
        for n,(st,d) in ex.map(run, range(8,21)): print(f"n={n} K4 {st} {d}",flush=True)

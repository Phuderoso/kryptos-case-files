"""Cycle 198 decoder: each M line (stdin: 'srcbin N kind M ...'), decoded with lib197 under EVERY d that gives the same crib record (I-223)
and, for a one-error fit, under EVERY slot whose deletion gives the same 2-core (the same one-error event; lib198.equivalent_slots), with
that slot removed; every consistent key (B: cyclic components, capped). Prints the best off-crib quadgram score per fit.
usage: decode198.py CT quadgrams.json sup_dir < lines"""
import sys, json
from lib198 import *
ct, qf, sup = sys.argv[1:4]; D = sup
Q = json.load(open(qf)); QQ, FL = Q["q"], Q["floor"]
def score(pt, N):
    crib = set(CI); tot = cnt = 0
    for k in range(N - 3):
        s = pt[k:k + 4]
        if "?" in s or any(k + j in crib for j in range(4)): continue
        tot += QQ.get(s, FL); cnt += 1
    return (tot / cnt if cnt else -99), cnt
for line in sys.stdin:
    if not line.strip(): continue
    src, N, kind, mline = line.split(None, 3); N = int(N); w = mline.split()
    solver = w[1]; q, d, model = int(w[3]), int(w[4]), w[5]
    ab, form, m, n, slot = w[6], w[7], int(w[8]), int(w[9]), int(w[11])
    if src == "direct":
        rec = rec_from_file(f"{D}/recs197_direct.txt", q); tags = kind_from_map(f"{D}/recs197_direct_map.txt", q)[2]
        alts = [(t.split()[1], int(t.split()[2])) for t in tags]
    else:
        out = load_perm(f"{sup}/{src}.bin", N, q); rec = perm_record(out, kind, d)
        alts = [(kind, dd) for dd in range(N if kind == "del" else N + 1) if perm_record(out, kind, dd) == rec]
    slots = equivalent_slots(rec, model, m, n, slot) if slot >= 0 else [None]
    best = None; nd = 0
    for s in slots:
        r2 = drop_slot(rec, [s] if s is not None else [])
        for (kk, dd) in alts:
            NN = 98 if kk == "del" else 96
            o = list(range(NN)) if src == "direct" else out
            for pt in decode(ct, o, NN, kk, dd, r2, model, solver, ab, form, m, n, maxsol=26):
                nd += 1; sc, c = score(pt, NN)
                if best is None or sc > best[0]: best = (sc, c, pt, kk, dd, s)
    if best is None: print("INCONSISTENT", mline.strip()); continue
    sc, c, pt, kk, dd, s = best
    print(f"{mline.strip()} | src {src} | decodes {nd} over {len(alts)} d x {len(slots)} slots | best d {dd} slot {s} quad {sc:.2f} on {c} | {pt}")

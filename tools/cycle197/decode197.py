"""Cycle 197 decoder: every M line given (stdin: 'file<TAB>M line' or plain M lines with --src), decoded with lib197 under EVERY d that
gives the same crib record (the off-crib text depends on d) and every consistent key (B: cyclic components, capped). Prints the best
off-crib quadgram score (mean log10 per quadgram over runs of determined letters, cribs excluded) per fit.
usage: decode197.py CT quadgrams.json sup_dir recs_dir < lines   (line: srcbin N kind | M ...)"""
import sys, json
from lib197 import *
ct, qf, sup, D = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
ALN = {}
try:
    for l in open(f"{sup}/alpha_direct189.txt"):
        a, b = l.split()[:2]; ALN[b] = a
except OSError: pass
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
    ab, form, m, n = w[6], w[7], int(w[8]), int(w[9])
    if solver == "A" and ab not in ("AZ", "KA"): ab = ALN[ab]
    if src == "direct":
        rec = rec_from_file(f"{D}/recs197_direct.txt", q); tags = kind_from_map(f"{D}/recs197_direct_map.txt", q)[2]
        alts = [(t.split()[1], int(t.split()[2])) for t in tags]; outs = None
    else:
        out = load_perm(f"{sup}/{src}.bin", N, q); rec = perm_record(out, kind, d)
        alts = [(kind, dd) for dd in range(N if kind == "del" else N + 1) if perm_record(out, kind, dd) == rec]
    best = None; nd = 0
    for (kk, dd) in alts:
        NN = 98 if kk == "del" else 96
        o = list(range(NN)) if src == "direct" else out
        for pt in decode(ct, o, NN, kk, dd, rec, model, solver, ab, form, m, n, maxsol=26):
            nd += 1; s, c = score(pt, NN)
            if best is None or s > best[0]: best = (s, c, pt, kk, dd)
    if best is None: print("INCONSISTENT", mline.strip()); continue
    s, c, pt, kk, dd = best
    print(f"{mline.strip()} | src {src} | decodes {nd} over {len(alts)} equivalent d | best d {dd} quad {s:.2f} on {c} | {pt}")

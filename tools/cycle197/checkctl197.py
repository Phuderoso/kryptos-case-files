"""Cycle 197 control checker (independent of cmp197): for each plant, rebuild the planted record in Python (lib197), find solver M lines
in the planted cell (solver, model, alph/tab, form, m, n) whose record (rebuilt in Python from the reported q, d) EQUALS the planted record,
and decode the reported config with lib197.decode: the planted plaintext must be reproduced at every determined position (and >= 1
determined position off the cribs). Negatives: report every M line at the planted record in any cell."""
import sys
from lib197 import *
ctl, outf, sup, D = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
M = {}
for line in open(outf):
    w = line.split()
    if w[0] == "M": M.setdefault(w[2], []).append(w)
recf, mapf = f"{D}/recs197_direct.txt", f"{D}/recs197_direct_map.txt"
def R2kp(kind, d):
    if kind == "del": return [j if j < d else j + 1 for j in CI]
    return [j if j < d else (0 if j == d else j - 1) for j in CI]
npass = ntot = 0
for line in open(ctl):
    nm, ct, src, N, kind, d, q, model, solver, ab, form, m, n, keys, P = line.split(); N, d, q, m, n = map(int, (N, d, q, m, n))
    direct = src.startswith("direct")
    if direct:
        out = list(range(N))
        if src == "directR2": kp = R2kp(kind, d); cv = [(-1 if (kind == "ins" and j == d) else j) for j in CI]
        else: kp = CI[:]; cv = [carved_of(i, kind if N != 97 else "none", d) for i in CI]
        if N == 97: kind, N, d = "del", 98, 97; out = list(range(98))    # indel-free plant = the del record with the dropped letter after the text
        prec = [kp, kp, cv]
    else:
        out = load_perm(f"{sup}/{src}.bin", N, q); prec = perm_record(out, kind, d)
    hits = []
    for w in M.get(nm, []):
        rq, rd, rmd, rab, rfm, rm, rn = int(w[3]), int(w[4]), w[5], w[6], w[7], int(w[8]), int(w[9])
        if direct: rec = rec_from_file(recf, rq); rkind, rdd, tags = kind_from_map(mapf, rq)
        else:
            if rq != q: continue
            rec = perm_record(out, kind, rd); rkind, rdd = kind, rd
        same = (rec[2] == prec[2]) and ((rec[0] == prec[0]) if rmd in "PD" else (rec[1] == prec[1]))
        if not same: continue
        hits.append((w, rec, rkind, rdd))
    neg = nm.startswith("N"); ntot += 1
    if neg:
        print(f"{nm} NEGATIVE: {len(hits)} solver fits at the planted record:", [" ".join(h[0][1:]) for h in hits][:5])
        npass += len(hits) == 0 or all(float(h[0][-2 if h[0][1]=='B' else -1]) > 0.0 for h in hits) and False or len(hits) == 0
        continue
    good = None
    for (w, rec, rkind, rdd) in hits:
        if (w[1], w[6], w[7], int(w[8]), int(w[9])) != (solver, ab, form, m, n) or (not direct and w[5] != model): continue
        # a record stands for every (kind, d) that gives it; the off-crib decryption depends on d, so decode under each
        if direct:
            alts = [(t.split()[1], int(t.split()[2])) for t in kind_from_map(mapf, int(w[3]))[2]]
        else:
            alts = [(kind, dd) for dd in range((N if kind == "del" else N + 1)) if perm_record(out, kind, dd) == rec]
        pts = []
        for (kk, dd) in alts:
            NN = 98 if kk == "del" else 96
            pts += decode(ct, list(range(NN)) if direct else out, NN, kk, dd, rec, w[5], solver, ab, form, m, n, maxsol=64)
        for pt in pts:
            if len(pt) != N: continue
            det = [k for k in range(N) if pt[k] != "?"]
            if det and all(pt[k] == P[k] for k in det) and any(k not in CI for k in det):
                good = (w, pt, len(det)); break
        if good: break
    if good:
        npass += 1; print(f"{nm} PASS: {' '.join(good[0][1:])} | determined {good[2]}/{N} | {good[1][:60]}")
    else: print(f"{nm} FAIL: {len(hits)} fits at planted record; none decodes to the plant")
print(f"controls {npass}/{ntot}")

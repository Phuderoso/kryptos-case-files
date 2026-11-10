"""Cycle 198 control checker (independent of cmp198): rebuild the planted record in Python, find the solver's M lines in the planted cell at
that record, require the reported slot to be the planted wrong slot or one giving the same one-error event (same 2-core, lib198), and decode
with the planted wrong slot removed (lib197.decode, every equivalent d): the planted plaintext must be reproduced at every determined position
except the carved position(s) of the altered letter. P1s (no wrong letter) must be found with slot -1. Negatives (N3, N4 two wrong letters;
N1 three keys) must give no fit at the planted record in the planted cell (N1: in any cell)."""
import sys
from lib198 import *
ctl, outf, sup, D = sys.argv[1:5]
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
    nm, ct, src, N, kind, d, q, model, solver, ab, form, m, n, keys, wrong, P = line.split(); N, d, q, m, n = map(int, (N, d, q, m, n))
    wrong = [] if wrong == "-" else list(map(int, wrong.split(",")))
    direct = src.startswith("direct")
    if direct:
        out = list(range(N))
        if src == "directR2": kp = R2kp(kind, d); cv = [(-1 if (kind == "ins" and j == d) else j) for j in CI]
        else: kp = CI[:]; cv = [carved_of(i, kind, d) for i in CI]
        prec = [kp, kp, cv]
    else:
        out = load_perm(f"{sup}/{src}.bin", N, q); prec = perm_record(out, kind, d)
    badcarved = {prec[2][t] for t in wrong}
    hits = []
    for w in M.get(nm, []):
        rq, rd, rmd, rab, rfm, rm, rn, slot = int(w[3]), int(w[4]), w[5], w[6], w[7], int(w[8]), int(w[9]), int(w[11])
        if direct: rec = rec_from_file(recf, rq)
        else:
            if rq != q: continue
            rec = perm_record(out, kind, rd)
        same = (rec[2] == prec[2]) and ((rec[0] == prec[0]) if rmd in "PD" else (rec[1] == prec[1]))
        if same: hits.append((w, rec, slot))
    ntot += 1
    incell = [h for h in hits if (h[0][1], h[0][6], h[0][7], int(h[0][8]), int(h[0][9])) == (solver, ab, form, m, n) and (direct or h[0][5] == model)]
    if nm.startswith("N"):
        bad = incell
        print(f"{nm} NEGATIVE: {len(bad)} fits at the planted record in the planted cell:", [" ".join(h[0][1:]) for h in bad][:4],
              f"| fits at the planted record in other cells (chance, reported): {len(hits) - len(incell)}", [" ".join(h[0][1:]) for h in hits if h not in incell][:3])
        npass += len(bad) == 0; continue
    good = None
    for (w, rec, slot) in incell:
        if wrong:
            eq = equivalent_slots(rec, w[5], m, n, wrong[0])
            if slot not in eq and not (nm == "P1b" and slot == -1): continue
        elif slot != -1: continue
        if direct: alts = [(t.split()[1], int(t.split()[2])) for t in kind_from_map(mapf, int(w[3]))[2]]
        else: alts = [(kind, dd) for dd in range((N if kind == "del" else N + 1)) if perm_record(out, kind, dd) == rec]
        for (kk, dd) in alts:
            NN = 98 if kk == "del" else 96
            if NN != N: continue
            o = list(range(NN)) if direct else out
            for pt in decode(ct, o, NN, kk, dd, drop_slot(rec, wrong), w[5], solver, ab, form, m, n, maxsol=64):
                det = [k for k in range(N) if pt[k] != "?" and carved_of(o[k], kk, dd) not in badcarved]
                if det and all(pt[k] == P[k] for k in det) and any(k not in CI for k in det):
                    good = (w, pt, len(det)); break
            if good: break
        if good: break
    if good: npass += 1; print(f"{nm} PASS: {' '.join(good[0][1:])} | wrong slot {wrong or '-'} | determined {good[2]}/{N} | {good[1][:60]}")
    else: print(f"{nm} FAIL: {len(hits)} fits at planted record ({len(incell)} in cell); none passes")
print(f"controls {npass}/{ntot}")

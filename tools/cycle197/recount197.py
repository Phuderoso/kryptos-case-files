"""Cycle 197 independent recount (no union-find: BFS propagation with exhaustive roots, lib197.solve_bij, tables built here).
usage: recount197.py CT stage src N kind pairsfile solver maxq [mmax_plus_n]
  stage direct: src = records file (model D); stage perm: src = perm bank (models P and C), first maxq perms, every d of the record runs.
Prints 'R solver model ab form m n fits' per cell (fits only; compare with cmp197 H lines on the same subset)."""
import sys, collections
from multiprocessing import Pool
from lib197 import *
ct, stage, src, N, kind, pf, solver, maxq = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7], int(sys.argv[8])
lim = int(sys.argv[9]) if len(sys.argv) > 9 else 99
pairs = [(l.split()[0], int(l.split()[1]), int(l.split()[2])) for l in open(pf) if l.strip()]
pairs = [p for p in pairs if p[1] + p[2] <= lim]
if stage == "direct": pairs = [p for p in pairs if p[0] == "P"]
ABS = ["AZ", "KA"] if solver == "A" else ["AZ>KA", "KA>AZ"]
FORMS = ["vig", "beau"] if solver == "A" else ["VV", "VB", "BV", "BB"]
# lookup: TB[(ab, form, t, letter)] = (fwd list, bwd list)
TB = {}
for ab in ABS:
    for form in FORMS:
        for t in range(24):
            for L in AZ:
                if solver == "A":
                    al = AZ if ab == "AZ" else KA; K = keyval_add(form, al, PTC[t], L)
                    f = [(K - a) % 26 for a in range(26)]; TB[(ab, form, t, L)] = (f, f)
                else:
                    f = [0] * 26; g = [0] * 26
                    for a in range(26):
                        for b in range(26):
                            if enc_two(ab, form, PTC[t], a, b) == L: f[a] = b; g[b] = a
                    TB[(ab, form, t, L)] = (f, g)
def records():
    if stage == "direct":
        for line in open(src):
            w = list(map(int, line.split())); yield [w[2:26], w[2:26], w[26:50]]
    else:
        import struct
        raw = open(src, "rb").read(); nperm = min(maxq, len(raw) // (2 * N))
        for q in range(nperm):
            out = list(struct.unpack(f"<{N}h", raw[q * 2 * N:(q + 1) * 2 * N])); seen = set()
            for d in range(N if kind == "del" else N + 1):
                r = perm_record(out, kind, d); key = tuple(r[2])
                if key in seen: continue
                seen.add(key); yield r
def work(rec):
    cnt = collections.Counter()
    for (md, m, n) in pairs:
        if stage == "direct": model = "D"; pos = rec[0]
        else: model = md; pos = rec[0] if md == "P" else rec[1]
        edges = [(pos[t] % m, pos[t] % n, t) for t in range(24) if rec[2][t] >= 0]
        for ab in ABS:
            for form in FORMS:
                tb = {t: TB[(ab, form, t, ct[rec[2][t]])] for (_, _, t) in edges}
                ok, _ = solve_bij(edges, m, n, lambda t, a: tb[t][0][a], lambda t, b: tb[t][1][b])
                if ok: cnt[(model, ab, form, m, n)] += 1
    return cnt
if __name__ == "__main__":
    tot = collections.Counter()
    with Pool(8) as p:
        for c in p.imap_unordered(work, list(records()), chunksize=16): tot.update(c)
    for (model, ab, form, m, n) in sorted(set((("D" if stage == "direct" else md), ab, fm, m, n) for (md, m, n) in pairs for ab in ABS for fm in FORMS)):
        print("R", solver, model, ab, form, m, n, tot[(model, ab, form, m, n)])

"""Cycle 166 language check of model-T fits (three independent period-7 keys).  For each T line: crib list as in
split3 (sorted by key index), segment 1 = cribs [0,e), segment 3 = cribs [s,n), segment 2 = the rest; boundaries
placed at the first crib of segments 2 and 3 (b1 = X[e], b2 = X[s]); each segment's key values come from its cribs,
'?' where a residue has no crib in its segment.  Plaintext P[i] = dec(C[S[i]], key at idx(i)), idx = i (direct /
model Q) or S[i] (carved index).  Score: mean log10 quadgram over fully determined quadgrams, all and off-crib.
usage: decode166.py CT label file...   (reads T lines; D-prefixed one-error lines are skipped)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(int)
Q = np.fromfile("/home/box/kryptos_support_backup/quad.bin", dtype=np.float32)
B = np.memmap("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16, mode='r').reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"; CR = set(CI)
def score(t, skip=False):
    v = [Q[sum((ord(c) - 65) * 26 ** (3 - z) for z, c in enumerate(t[i:i + 4]))] for i in range(94)
         if '?' not in t[i:i + 4] and not (skip and any(j in CR for j in range(i, i + 4)))]
    return (float(np.mean(v)) if v else -99.0), len(v)
def decode(ct, q, d, ix, a, forms, e, s):
    S = list(range(97)) if q < 0 else ([int(x) for x in B[q]] if d == 0 else [int(x) for x in np.argsort(B[q])])
    A = AL[a]; inv = np.zeros(26, int); inv[A] = np.arange(26)
    cr = sorted(((S[CI[t]] if ix else CI[t]), ord(ct[S[CI[t]]]) - 65, ord(PT[t]) - 65) for t in range(24))
    X = [c[0] for c in cr]; b1 = X[e] if e < 24 else 97; b2 = X[s] if s < 24 else 97
    seg = lambda x: 0 if x < b1 else (1 if x < b2 else 2)
    key = [[None] * 7 for _ in range(3)]
    for x, c, p in cr:
        g = seg(x); m = forms[g]; key[g][x % 7] = (inv[c] - inv[p]) % 26 if m == 0 else (inv[c] + inv[p]) % 26
    out = []
    for i in range(97):
        x = S[i] if ix else i; g = seg(x); k = key[g][x % 7]; c = inv[ord(ct[S[i]]) - 65]
        out.append('?' if k is None else chr(65 + A[(c - k) % 26 if forms[g] == 0 else (k - c) % 26]))
    return ''.join(out)
if __name__ == "__main__":
    ct, lab = sys.argv[1], sys.argv[2]; rows = []
    for fn in sys.argv[3:]:
        for line in open(fn):
            f = line.split()
            if f[0] != 'T' or f[-1] != '3': continue
            q, d, ix, a = int(f[2]), int(f[3]), int(f[4]), int(f[5])
            if fn.endswith('.txt') and '/D_' in fn: q = -1
            forms = [int(f[6]), int(f[7]), int(f[8])]; e, s = int(f[9]), int(f[10])
            t = decode(ct, q, d, ix, a, forms, e, s)
            assert all(t[CI[k]] == PT[k] for k in range(24)), (line, t)
            sc, nq = score(t); so, no = score(t, True); rows.append((so, sc, nq, line.strip(), t))
    rows.sort(reverse=True)
    best = rows[0] if rows else None
    print(f"DEC {lab} fits={len(rows)} best_offcrib={best[0] if best else 'NA':.3f} best_all={best[1] if best else 'NA':.3f}" if best else f"DEC {lab} fits=0")
    for r in rows[:3]: print(f"  {r[0]:.3f} {r[1]:.3f} nq={r[2]} {r[3]}\n  {r[4]}")

"""Cycle 78: periodic keyword key plus a per-carved-row shift (K4 on the copper's own 31-letter rows).
k_i = A[a(i)] + B[row(i)] (mod 26, in tableau index space), A of period p (1..31), B arbitrary per carved row.
Model R (restart): a(i) = col(i) mod p  (keyword restarts at the start of every carved row)
Model C (continue): a(i) = i mod p      (keyword runs on, the row adds a shift)
Start column of K4 on its first carved row: 27 (counting '?') or 26 (not counting it).
Vigenere / Beaufort / variant on KA and A-Z tableaux. Exact weighted union-find on the 24 crib letters."""
import sys, json, random
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Q = json.load(open("/workspace/k4c25/quadgrams.json")); qf, qq = Q["floor"], Q["q"]
cpos = list(range(21, 34)) + list(range(63, 74)); crib = "EASTNORTHEAST" + "BERLINCLOCK"
def solve(ct, T, mode, model, p, start, want_partial=False):
    ix = {c: n for n, c in enumerate(T)}
    par, val = {}, {}
    def find(x):
        if par.setdefault(x, x) == x: return x, 0
        r, d = find(par[x]); par[x] = r; val[x] = (val.get(x, 0) + d) % 26; return r, val[x]
    def pos(i):
        g = i + start; return g % 31, g // 31
    def nodes(i):
        col, row = pos(i); a = (col % p) if model == "R" else (i % p); return ("A", a), ("B", row)
    checks = 0
    for i, pc in zip(cpos, crib):
        c, q = ix[ct[i]], ix[pc]
        k = (c - q) if mode == "V" else (c + q) if mode == "B" else (q - c)
        a, b = nodes(i)   # A_a - B'_b = k  (B' = -B)
        ra, da = find(a); rb, db = find(b)   # x = root + d
        if ra == rb:
            if (da - db) % 26 != k % 26: return None
            checks += 1
        else:
            par[ra] = rb; val[ra] = (db + k - da) % 26
    if not want_partial: return checks, None
    out = []
    for i in range(97):
        a, b = nodes(i); ra, da = find(a); rb, db = find(b)
        if ra != rb: out.append("."); continue
        k = (da - db) % 26; c = ix[ct[i]]
        q = (c - k) if mode == "V" else (k - c) if mode == "B" else (c + k)
        out.append(T[q % 26])
    return checks, "".join(out)
def qscore(s):
    sc = [qq.get(s[i:i+4], qf) for i in range(len(s) - 3) if "." not in s[i:i+4]]
    return (sum(sc) / len(sc), len(sc)) if sc else (None, 0)
def sweep(ct, partial=False):
    res = []
    for T, tn in ((KA, "KA"), (AZ, "AZ")):
        for mode in "VBX":
            for model in "RC":
                for start in (26, 27):
                    for p in range(1, 32):
                        r = solve(ct, T, mode, model, p, start, partial)
                        if r: res.append((r[0], tn, mode, model, start, p, r[1]))
    return res
if __name__ == "__main__":
    rng = random.Random(78)
    report = {}
    k4 = sweep(K4, True)
    report["k4_consistent"] = len(k4); report["k4_tests"] = 2*3*2*2*31
    best = sorted(k4, key=lambda r: -r[0])[:12]
    report["k4_best"] = []
    for r in best:
        s, n = qscore(r[6]); report["k4_best"].append(dict(checks=r[0], tableau=r[1], mode=r[2], model=r[3], start=r[4], p=r[5], partial=r[6], qg=s, n4=n))
    nulls = []
    for j in range(20):
        l = list(K4); rng.shuffle(l); res = sweep("".join(l))
        nulls.append(dict(consistent=len(res), max_checks=max([r[0] for r in res] + [-1])))
    report["nulls"] = nulls
    # planted controls: English plaintext with the cribs in place, random keyword A (period p) and random row shifts B
    src = open("eng.txt").read()
    ctl = []
    for j in range(8):
        T = rng.choice([KA, AZ]); mode = rng.choice("VBX"); model = rng.choice("RC"); start = rng.choice([26, 27]); p = rng.choice([5, 7, 8, 10, 11, 13])
        o = rng.randrange(0, len(src) - 100); pt = list(src[o:o+97])
        for i, c in zip(cpos, crib): pt[i] = c
        A = [rng.randrange(26) for _ in range(p)]; B = [rng.randrange(26) for _ in range(5)]
        ct = []
        for i in range(97):
            g = i + start; col, row = g % 31, g // 31; a = (col % p) if model == "R" else (i % p)
            k = (A[a] + B[row]) % 26; q = T.index(pt[i])
            c = (q + k) if mode == "V" else (k - q) if mode == "B" else (q - k)
            ct.append(T[c % 26])
        ct = "".join(ct); r = solve(ct, T, mode, model, p, start, True)
        tn = "KA" if T == KA else "AZ"
        allr = sweep(ct); rank = 1 + sum(1 for x in allr if r and x[0] > r[0])
        ctl.append(dict(tableau=tn, mode=mode, model=model, start=start, p=p, recovered=r is not None, checks=r[0] if r else None,
                        rank_by_checks=rank, qg=qscore(r[1])[0] if r else None, partial=r[1] if r else None))
    report["controls"] = ctl
    json.dump(report, open("cycle78_summary.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "k4_best"}, indent=0)[:3000])
    for b in report["k4_best"]: print(b)

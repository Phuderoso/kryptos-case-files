"""Cycle 176: decode and English-score every reported fit (M lines of gm176 / pg176).
Score = mean log10 quadgram over off-crib windows (as decode173/175.py). Model G fixes the cipher alphabet only on the letters
that occur under the cribs; the free letters get the free alphabet values by a seeded hill-climb on the score (same budget for
every text: RESTARTS x ITERS swaps), so the reported score is an upper bound over the free part. PG fits are fully determined.
Every fit is also REPLAYED here from the definitions (string level), independently of the C code: a fit that does not replay is
reported as BAD.
usage: decode176.py CT perms.bin quadgrams.json cfg176.txt label outfile [M-files...]"""
import sys, json, random, numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; T = {"az": AZ, "ka": KA}
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
RESTARTS, ITERS = 3, 2500
ct, pf, qf, cfgf, lab, outf = sys.argv[1:7]
J = json.load(open(qf)); Q = J["q"]; FL = J["floor"]
P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
def score(s):
    v = [Q.get(s[i:i + 4], FL) for i in range(94) if not any(i + k in CRIB for k in range(4))]
    return sum(v) / len(v)
def gstream(pr):
    d = [int(c) for c in pr]; L = len(d)
    while len(d) < 97: d.append((d[-L] + d[-L + 1]) % 10)
    return d
cfg = {}
def getcfg(name):
    if not cfg:
        for l in open(cfgf):
            a = l.split(); cfg[a[0]] = (a[1], a[2], [AZ.index(c) for c in a[3]])
    return cfg[name]
out = open(outf, "w"); n = 0; bad = 0
for mf in sys.argv[7:]:
    for l in open(mf):
        if not l.startswith("M "): continue
        a = l.split(); n += 1
        if len(a) >= 8 and a[3].isdigit():          # G: M lab ix L pa form q primer [name]
            ix, L, pa, form, q, pr = int(a[2]), int(a[3]), a[4], a[5], int(a[6]), a[7]
            PA = T[pa]; d = gstream(pr); S = [int(x) for x in P[q]]; sg = -1 if form == "beau" else 1
            kidx = (lambda i: i) if ix == 0 else (lambda i: S[i])       # key index of plaintext position i
            # replay: v(ct) = w over cribs must be a consistent bijection
            v = {}; inv = {}; ok = True
            for i, p in CRIB.items():
                c = ct[S[i]]; w = (PA.index(p) + d[kidx(i)]) % 26 if sg > 0 else (d[kidx(i)] - PA.index(p)) % 26
                if v.setdefault(c, w) != w or inv.setdefault(w, c) != c: ok = False
            if not ok: bad += 1; out.write("BAD " + l); continue
            freeL = [c for c in AZ if c not in v]; freeV = [x for x in range(26) if x not in inv]
            def dec(vv):
                s = []
                for i in range(97):
                    w = vv[ct[S[i]]]; k = d[kidx(i)]
                    s.append(PA[(w - k) % 26] if sg > 0 else PA[(k - w) % 26])
                return "".join(s)
            best = (-99, ""); R = random.Random(hash((lab, q, pr, pa, form, ix)) & 0xffffffff)
            for r in range(RESTARTS):
                fv = freeV[:]; R.shuffle(fv); vv = dict(v); vv.update(zip(freeL, fv)); cur = score(dec(vv))
                for it in range(ITERS):
                    if len(freeL) < 2: break
                    x, y = R.sample(freeL, 2); vv[x], vv[y] = vv[y], vv[x]; sc = score(dec(vv))
                    if sc >= cur: cur = sc
                    else: vv[x], vv[y] = vv[y], vv[x]
                if cur > best[0]: best = (cur, dec(vv))
            out.write(f"G {lab} ix{ix} L{L} {pa} {form} q{q} {pr} {' '.join(a[8:])} fixed={26-len(freeL)} score={best[0]:.3f} {best[1]}\n")
        else:                                       # PG: M lab ix form q cfg
            ix, form, q, name = int(a[2]), a[3], int(a[4]), a[5]
            CA, PAs, k = getcfg(name); S = [int(x) for x in P[q]]; kidx = (lambda i: i) if ix == 0 else (lambda i: S[i])
            s = "".join(PAs[(CA.index(ct[S[i]]) - k[kidx(i)]) % 26] if form == "vig" else PAs[(k[kidx(i)] - CA.index(ct[S[i]])) % 26] for i in range(97))
            ok = all(s[i] == p for i, p in CRIB.items())
            if not ok: bad += 1; out.write("BAD " + l); continue
            out.write(f"P {lab} ix{ix} {form} q{q} {name} score={score(s):.3f} {s}\n")
out.write(f"END {lab} fits={n} bad={bad}\n")

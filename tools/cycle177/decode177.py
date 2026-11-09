"""Cycle 177: replay and decode every reported fit (M lines of gm177 / pg177), cycle 176's procedure extended to one error.
Score = mean log10 quadgram over off-crib windows. Model G fixes the cipher alphabet only on the letters under the cribs; the
free letters are filled by a seeded hill-climb (RESTARTS x ITERS swaps, same budget for every text), so the score is an upper
bound over the free part. For a one-error fit every slot t in the drop mask is tried as the wrong slot (that slot is left out of
the replay and of the fixed letters) and the best decode is kept. Every fit is REPLAYED here from the definitions (string level,
independent of the C code); a fit that does not replay on the 23 (or 24) slots is reported as BAD. PG fits are fully determined
and must match >= 23 of 24 crib letters.
usage: decode177.py CT perms.bin quadgrams.json cfg176.txt label outfile maxL_ix0 [M-files...]   (G ix 0 fits with L > maxL_ix0
are skipped, per the pre-registration; named primers have L = their length and are always decoded)"""
import sys, json, random, numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; T = {"az": AZ, "ka": KA}
CIL = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
CRIB = {i: PT[t] for t, i in enumerate(CIL)}
RESTARTS, ITERS = 3, 2500
ct, pf, qf, cfgf, lab, outf, maxL0 = sys.argv[1:8]; maxL0 = int(maxL0)
J = json.load(open(qf)); Q = J["q"]; FL = J["floor"]
P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
def score(s):
    v = [Q.get(s[i:i + 4], FL) for i in range(94) if not any(i + k in CRIB for k in range(4))]
    return sum(v) / len(v)
def gstream(pr, b):
    d = [int(c) for c in pr]; L = len(d)
    while len(d) < 97: d.append((d[-L] + d[-L + 1]) % b)
    return d
cfg = {}
def getcfg(name):
    if not cfg:
        for l in open(cfgf):
            a = l.split(); cfg[a[0]] = (a[1], a[2], [AZ.index(c) for c in a[3]])
    return cfg[name]
out = open(outf, "w"); n = 0; bad = 0; skipped = 0
for mf in sys.argv[8:]:
    for l in open(mf):
        if not l.startswith("M "): continue
        a = l.split()
        if len(a) >= 10:                              # G: M lab ix L pa form base q primer mask [name]
            ix, L, pa, form, b, q, pr, mask = int(a[2]), int(a[3]), a[4], a[5], int(a[6]), int(a[7]), a[8], int(a[9], 16)
            if ix == 0 and len(a) == 10 and L > maxL0: skipped += 1; continue
            n += 1
            PA = T[pa]; d = gstream(pr, b); S = [int(x) for x in P[q]]; sg = -1 if form == "beau" else 1
            kidx = (lambda i: i) if ix == 0 else (lambda i: S[i])
            drops = [None] if mask == 0xFFFFFF else [t for t in range(24) if (mask >> t) & 1]
            best = (-99, "", None, 0); anyok = False
            for drop in drops:
                v = {}; inv = {}; ok = True
                for t, i in enumerate(CIL):
                    if t == drop: continue
                    c = ct[S[i]]; p = PT[t]; w = (PA.index(p) + d[kidx(i)]) % 26 if sg > 0 else (d[kidx(i)] - PA.index(p)) % 26
                    if v.setdefault(c, w) != w or inv.setdefault(w, c) != c: ok = False
                if not ok: continue
                anyok = True
                freeL = [c for c in AZ if c not in v]; freeV = [x for x in range(26) if x not in inv]
                def dec(vv):
                    return "".join(PA[(vv[ct[S[i]]] - d[kidx(i)]) % 26] if sg > 0 else PA[(d[kidx(i)] - vv[ct[S[i]]]) % 26] for i in range(97))
                R = random.Random(hash((lab, q, pr, pa, form, ix, b, drop)) & 0xffffffff)
                for r in range(RESTARTS):
                    fv = freeV[:]; R.shuffle(fv); vv = dict(v); vv.update(zip(freeL, fv)); cur = score(dec(vv))
                    for it in range(ITERS):
                        if len(freeL) < 2: break
                        x, y = R.sample(freeL, 2); vv[x], vv[y] = vv[y], vv[x]; sc = score(dec(vv))
                        if sc >= cur: cur = sc
                        else: vv[x], vv[y] = vv[y], vv[x]
                    if cur > best[0]: best = (cur, dec(vv), drop, 26 - len(freeL))
            if not anyok: bad += 1; out.write("BAD " + l); continue
            out.write(f"G {lab} ix{ix} L{L} {pa} {form} b{b} q{q} {pr} {' '.join(a[10:])} mask={a[9]} drop={best[2]} fixed={best[3]} score={best[0]:.3f} {best[1]}\n")
        else:                                         # PG: M lab ix form q cfg miss
            n += 1
            ix, form, q, name, miss = int(a[2]), a[3], int(a[4]), a[5], int(a[6])
            CA, PAs, k = getcfg(name); S = [int(x) for x in P[q]]; kidx = (lambda i: i) if ix == 0 else (lambda i: S[i])
            s = "".join(PAs[(CA.index(ct[S[i]]) - k[kidx(i)]) % 26] if form == "vig" else PAs[(k[kidx(i)] - CA.index(ct[S[i]])) % 26] for i in range(97))
            nm = sum(s[i] == p for i, p in CRIB.items())
            if nm < 23: bad += 1; out.write("BAD " + l); continue
            out.write(f"P {lab} ix{ix} {form} q{q} {name} miss={miss} match={nm} score={score(s):.3f} {s}\n")
out.write(f"END {lab} fits={n} bad={bad} skipped={skipped}\n")

"""Cycle 93: Bifid on a 5x5 square over the W-FREE 92-letter K4 text (W treated as a null, as in cycles 88-92).
Square: ANY placement of the 25 W-less letters. Cribs on the W-free text: EASTNORTHEAST at 20-32, BERLINCLOCK at 60-70.
Every period 1..92, both orientations (orient 0: ct = Bifid_enc(pt); orient 1: pt = Bifid_enc(ct), i.e. the
'decrypt' direction used as encryption).  Two models:
  'one': classic Bifid, one square;
  'two': independent input and output squares (= Bifid followed by any monoalphabetic substitution on 25 letters).
Exact SAT (CaDiCaL via PySAT), adapted from tools/k4_bifid6_sat.py (cycle 43). Only necessary conditions are encoded,
so UNSAT proves exclusion.  usage: bifid5w.py k4|nulls|controls"""
import random, sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from kryptos_text import K4
SYM = "ABCDEFGHIJKLMNOPQRSTUVXYZ"   # 25, no W
assert len(SYM) == 25
KW = K4.replace("W", ""); assert len(KW) == 92 and set(KW) == set(SYM)
CRIB = {20 + i: ch for i, ch in enumerate("EASTNORTHEAST")}
CRIB.update({60 + i: ch for i, ch in enumerate("BERLINCLOCK")})

def equalities(ct, crib, p, orient):
    n = len(ct); eq = []
    for b in range(0, n, p):
        L = min(p, n - b)
        for k in range(L):
            for q in range(2):
                j = 2 * k + q; ax, pi = j // L, j % L
                if orient == 0:
                    if (b + pi) in crib: eq.append(((1, ct[b + k], q), (0, crib[b + pi], ax)))
                else:
                    if (b + k) in crib: eq.append(((1, crib[b + k], q), (0, ct[b + pi], ax)))
    return eq

def consistent(ct, crib, p, orient, mode, want_model=False):
    eq = equalities(ct, crib, p, orient)
    top = [0]; cl = []
    def nv(): top[0] += 1; return top[0]
    nsq = 1 if mode == "one" else 2
    X = [[[nv() for c in range(25)] for s in range(25)] for _ in range(nsq)]
    for q in range(nsq):
        for grp in [X[q][s] for s in range(25)] + [[X[q][s][c] for s in range(25)] for c in range(25)]:
            e = CardEnc.equals(grp, 1, top_id=top[0], encoding=EncType.seqcounter)
            cl += e.clauses; top[0] = max(top[0], e.nv)
    D = {}
    def dig(sq, s, a, v):
        sq = 0 if mode == "one" else sq
        key = (sq, s, a, v)
        if key not in D:
            d = nv(); D[key] = d
            ts = [X[sq][SYM.index(s)][c] for c in range(25) if (c // 5, c % 5)[a] == v]
            cl.append([-d] + ts)
            for x in ts: cl.append([d, -x])
        return D[key]
    for (q1, s1, a1), (q2, s2, a2) in eq:
        for v in range(5):
            x, y = dig(q1, s1, a1, v), dig(q2, s2, a2, v); cl.append([-x, y]); cl.append([x, -y])
    with Cadical153(bootstrap_with=cl) as S:
        return S.solve()

def bifid_enc(pt, sqin, sqout, p):
    pos = {s: (i // 5, i % 5) for i, s in enumerate(sqin)}
    inv = {(i // 5, i % 5): s for i, s in enumerate(sqout)}
    out = []
    for b in range(0, len(pt), p):
        blk = pt[b:b + p]; L = len(blk)
        st = [pos[c][a] for a in range(2) for c in blk]
        out += [inv[(st[2 * k], st[2 * k + 1])] for k in range(L)]
    return "".join(out)

def scan(ct, label, mode, periods=range(1, 93)):
    res = {o: [p for p in periods if consistent(ct, CRIB, p, o, mode)] for o in (0, 1)}
    print(f"[{mode}] {label}: enc-orient {len(res[0])}/92 {res[0]}; dec-orient {len(res[1])}/92 {res[1]}", flush=True)
    return res

if __name__ == "__main__":
    which = sys.argv[1]; out = {}
    rng = random.Random(93)
    if which == "k4":
        for mode in ("one", "two"): out[mode] = scan(KW, "K4 W-free", mode)
    elif which == "nulls":
        for r in range(5):
            l = list(KW); rng.shuffle(l); s = "".join(l)
            for mode in ("one", "two"): out[f"null{r}_{mode}"] = scan(s, f"shuffled W-free null {r}", mode)
    elif which == "controls":
        filler = [c for c in "THEVALLEYLAYSILENTUNDERTHEOLDSTONESANDTHEBURIEDROOMHELDACANDLEFLAMEFLICKERINGINTHEDARKAIR" * 2]
        pt = "".join(CRIB[i] if i in CRIB else filler.pop(0) for i in range(92))
        assert "W" not in pt
        for p, mode, o in ((5, "one", 0), (11, "one", 1), (21, "one", 0), (7, "two", 0), (13, "two", 1)):
            sqin = list(SYM); rng.shuffle(sqin)
            sqout = sqin if mode == "one" else rng.sample(SYM, 25)
            if o == 0: ct = bifid_enc(pt, sqin, sqout, p)
            else:
                # orient 1 means pt = Bifid_enc(ct): build ct by inverting via brute search is hard; instead use
                # ct := Bifid_dec(pt) computed by inverse stream mapping
                pos = {s: (i // 5, i % 5) for i, s in enumerate(sqout)}; inv = {(i // 5, i % 5): s for i, s in enumerate(sqin)}
                ct = []
                for b in range(0, 92, p):
                    blk = pt[b:b + p]; L = len(blk)
                    st = [d for c in blk for d in pos[c]]
                    ct += [inv[(st[k], st[L + k])] for k in range(L)]
                ct = "".join(ct)
                assert bifid_enc(ct, sqin, sqout, p) == pt
            res = scan(ct, f"planted control p={p} orient={o}", mode)
            out[f"control_p{p}_{mode}_o{o}"] = {"ct": ct, "res": res, "true_hit": p in res[o]}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../data/cycle93/bifid5w_{which}.json"), "w"), indent=1)

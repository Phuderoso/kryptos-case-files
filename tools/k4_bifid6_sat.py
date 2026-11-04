"""Cycle 43: exact SAT test of Delastelle's Bifid on a 6x6 square (26 letters + 10 other signs, ARBITRARY placement),
every period 1..97, both orientations, two models:
  mode 'one': a single square (classic Bifid),
  mode 'two': independent input and output squares (= Bifid followed by any monoalphabetic substitution, or any
              5x5/6x6 Bifid whose output is re-lettered), the open item left by case file 20.
Each output letter's (row, col) equals two digits of the input coordinate stream (rows of the block, then cols);
where those input positions are cribbed this is an equality between square coordinates of two known letters.
Only necessary conditions are encoded (unknown plaintext may land on any cell), so UNSAT is a proof of exclusion."""
import random, sys, json
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from kryptos_text import K4
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYM = AZ + "0123456789"  # 36 signs fill the square (a bijection); K4 itself only uses the letters
CRIB = {21 + i: ch for i, ch in enumerate("EASTNORTHEAST")}
CRIB.update({63 + i: ch for i, ch in enumerate("BERLINCLOCK")})

def equalities(ct, crib, p, orient):
    """((sq,letter,axis),(sq,letter,axis)); sq 0 = input square, 1 = output square.
    orient 0: ct = Bifid_enc(pt); orient 1: pt = Bifid_enc(ct)."""
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

def consistent(ct, crib, p, orient, mode):
    eq = equalities(ct, crib, p, orient)
    if not eq: return True
    top = [0]; cl = []
    def nv(): top[0] += 1; return top[0]
    nsq = 1 if mode == "one" else 2
    X = [[[nv() for c in range(36)] for s in range(36)] for _ in range(nsq)]
    for q in range(nsq):
        for s in range(36):
            e = CardEnc.equals(X[q][s], 1, top_id=top[0], encoding=EncType.seqcounter).clauses
            cl += e; top[0] = max([top[0]] + [abs(l) for c in e for l in c])
        for c in range(36):
            e = CardEnc.equals([X[q][s][c] for s in range(36)], 1, top_id=top[0], encoding=EncType.seqcounter).clauses
            cl += e; top[0] = max([top[0]] + [abs(l) for c2 in e for l in c2])
    D = {}
    def dig(sq, s, a, v):
        sq = 0 if mode == "one" else sq
        key = (sq, s, a, v)
        if key not in D:
            d = nv(); D[key] = d
            ts = [X[sq][SYM.index(s)][c] for c in range(36) if (c // 6, c % 6)[a] == v]
            cl.append([-d] + ts)
            for x in ts: cl.append([d, -x])
        return D[key]
    for (q1, s1, a1), (q2, s2, a2) in eq:
        for v in range(6):
            x, y = dig(q1, s1, a1, v), dig(q2, s2, a2, v); cl.append([-x, y]); cl.append([x, -y])
    with Cadical153(bootstrap_with=cl) as S:
        return S.solve()

def bifid_enc(pt, sqin, sqout, p):
    pos = {s: (i // 6, i % 6) for i, s in enumerate(sqin) }
    inv = {(i // 6, i % 6): s for i, s in enumerate(sqout)}
    out = []
    for b in range(0, len(pt), p):
        blk = pt[b:b + p]; L = len(blk)
        st = [pos[c][a] for a in range(2) for c in blk]
        out += [inv[(st[2 * k], st[2 * k + 1])] for k in range(L)]
    return "".join(out)

def scan(ct, label, mode, periods=range(1, 98)):
    res = {o: [p for p in periods if consistent(ct, CRIB, p, o, mode)] for o in (0, 1)}
    print(f"[{mode}] {label}: enc-orient {len(res[0])}/97 {res[0]}; dec-orient {len(res[1])}/97 {res[1]}", flush=True)
    return res

if __name__ == "__main__":
    which = sys.argv[1]; out = {}
    rng = random.Random(43)
    if which == "k4":
        for mode in ("one", "two"): out[mode] = scan(K4, "K4", mode)
    elif which == "nulls":
        for r in range(5):
            l = list(K4); rng.shuffle(l); s = "".join(l)
            for mode in ("one", "two"): out[f"null{r}_{mode}"] = scan(s, f"shuffled-K4 null {r}", mode)
    elif which == "controls":
        filler = list("THEWALLFELLINTHENIGHTANDWEWALKEDTOWARDTHESQUAREUNDERTHEOLDWORLDCLOCKWHEREPEOPLESANGANDCRIEDLOUDLY" * 2)
        pt = "".join(CRIB[i] if i in CRIB else filler.pop(0) for i in range(97))
        for p, mode in ((5, "one"), (9, "one"), (17, "one"), (7, "two"), (13, "two")):
            sqin = list(SYM); rng.shuffle(sqin)
            sqout = sqin if mode == "one" else rng.sample(SYM, 36)
            ct = bifid_enc(pt, sqin, sqout, p)   # output may contain digit signs; the test treats them as symbols
            ok = consistent(ct, CRIB, p, 0, mode)
            out[f"control_p{p}_{mode}"] = {"ct": ct, "true_ok": ok, "res": scan(ct, f"planted control p={p} (true ok {ok})", mode)}
    json.dump(out, open(f"../analysis/cycle43_bifid6_{which}.json", "w"), indent=1)

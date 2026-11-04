"""Cycle 21: exact SAT test of Delastelle's Trifid (27-symbol 3x3x3 cube, ARBITRARY cube, 26 letters + one extra
symbol such as the carved '?'), every period 1..97, both orientations, against the 24 official crib letters.
Constraint: each ciphertext symbol's three cube digits equal three digits of the plaintext stream; where those
plaintext positions are cribbed, that is an equality between cube digits of two known symbols.
Also: census check that excludes every 25-letter (5x5 Polybius) output cipher, and Playfair self-encryption check."""
import random, sys, json
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from kryptos_text import K4
SYM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#"
TRI = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]
CRIB = {21 + i: ch for i, ch in enumerate("EASTNORTHEAST")}
CRIB.update({63 + i: ch for i, ch in enumerate("BERLINCLOCK")})

def equalities(ct, crib, p, orient):
    """Return list of ((sym1,axis1),(sym2,axis2)) equalities, orient 0: ct = Trifid_enc(pt), 1: pt = Trifid_enc(ct)."""
    n = len(ct); eq = []
    src, dst = (crib, None) if orient == 0 else (None, crib)
    for b in range(0, n, p):
        L = min(p, n - b)
        for k in range(L):
            for q in range(3):
                j = 3 * k + q; ax, pi = j // L, j % L
                if orient == 0:   # output symbol ct[b+k] digit q  ==  input pt[b+pi] digit ax
                    if (b + pi) in crib:
                        eq.append(((ct[b + k], q), (crib[b + pi], ax)))
                else:             # output pt[b+k] digit q == input ct[b+pi] digit ax
                    if (b + k) in crib:
                        eq.append(((crib[b + k], q), (ct[b + pi], ax)))
    return eq

def consistent(ct, crib, p, orient):
    eq = equalities(ct, crib, p, orient)
    if not eq: return True, 0
    vid = [0]
    def nv(): vid[0] += 1; return vid[0]
    X = [[nv() for t in range(27)] for s in range(27)]
    cl = []
    for s in range(27):
        cl += CardEnc.equals([X[s][t] for t in range(27)], 1, top_id=vid[0], encoding=EncType.seqcounter).clauses; vid[0] = max(vid[0], max(abs(l) for c in cl for l in c))
    for t in range(27):
        e = CardEnc.equals([X[s][t] for s in range(27)], 1, top_id=vid[0], encoding=EncType.seqcounter).clauses; cl += e; vid[0] = max(vid[0], max(abs(l) for c in e for l in c))
    D = {}
    def dig(s, a, v):
        key = (s, a, v)
        if key not in D:
            d = nv(); D[key] = d; ts = [X[SYM.index(s)][t] for t in range(27) if TRI[t][a] == v]
            cl.append([-d] + ts)
            for x in ts: cl.append([d, -x])
        return D[key]
    for (s1, a1), (s2, a2) in eq:
        for v in range(3):
            x, y = dig(s1, a1, v), dig(s2, a2, v); cl.append([-x, y]); cl.append([x, -y])
    with Cadical153(bootstrap_with=cl) as S:
        return S.solve(), len(eq)

def trifid_enc(pt, cube, p):
    pos = {s: TRI[i] for i, s in enumerate(cube)}; inv = {TRI[i]: s for i, s in enumerate(cube)}; out = []
    for b in range(0, len(pt), p):
        blk = pt[b:b + p]; L = len(blk)
        stream = [pos[c][a] for a in range(3) for c in blk]
        out += [inv[tuple(stream[3 * k:3 * k + 3])] for k in range(L)]
    return "".join(out)

def scan(ct, crib, label, periods=range(1, 98)):
    res = {}
    for o in (0, 1):
        res[o] = [p for p in periods if consistent(ct, crib, p, o)[0]]
    print(f"{label}: consistent periods enc-orient {len(res[0])}/97 {res[0]}; dec-orient {len(res[1])}/97 {res[1]}", flush=True)
    return res

if __name__ == "__main__":
    out = {}
    print("census: K4 distinct letters =", len(set(K4)), "-> every cipher whose output alphabet is a 25-cell 5x5 square (Playfair, Bifid, two-/four-square, Polybius letters) is impossible as K4's last layer")
    print("self-encryptions under cribs:", [(i, c) for i, c in CRIB.items() if K4[i] == c], "-> Playfair (never self-encrypts) also impossible on these alignments")
    out["K4"] = scan(K4, CRIB, "K4")
    rng = random.Random(21)
    for r in range(5):
        l = list(K4); rng.shuffle(l); out[f"null{r}"] = scan("".join(l), CRIB, f"shuffled-K4 null {r}")
    # planted controls: English 97-letter text with the cribs at official positions, random cube, period p
    base = ("THEWALLFELLANDWEWALKEDOUTXEASTNORTHEASTOFTHEGATEXTHENOONSUNSTOODOVERTHEBERLINCLOCKANDTHECROWDSANGLOUD")
    pt = "THEWALLFELLINTHENIGHTANDWEEASTNORTHEASTWALKEDTOWARDTHESQUAREUNDERTHEOLDWORLDBERLINCLOCKWHEREPEOPLESANGXX"[:97]
    # rebuild so cribs land exactly
    pt = list("X" * 97); filler = list("THEWALLFELLINTHENIGHTANDWEWALKEDTOWARDTHESQUAREUNDERTHEOLDWORLDCLOCKWHEREPEOPLESANGANDCRIEDLOUDLY" * 2)
    for i in range(97): pt[i] = filler.pop(0) if i not in CRIB else CRIB[i]
    pt = "".join(pt)
    for p in (4, 7, 11, 23):
        cube = list(SYM); rng.shuffle(cube); ct = trifid_enc(pt, cube, p)
        ct2 = ct.replace("#", "Q")  # keep letters only, as K4
        ok = consistent(ct, CRIB, p, 0)[0]
        r = scan(ct, CRIB, f"planted control period {p} (true period consistent: {ok})")
        out[f"control_p{p}"] = {"pt": pt, "ct": ct, "res": r, "true_ok": ok}
    json.dump(out, open("../analysis/trifid_sat_results.json", "w"), indent=1)

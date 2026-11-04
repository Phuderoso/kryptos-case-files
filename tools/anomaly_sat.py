"""Cycle 24: exact SAT (CaDiCaL), periodic key with BOTH alphabets arbitrary (Quagmire IV generalisation, covers
Quagmire I-III/Vigenere/Beaufort-type tableaux), on K4 with ONE carving anomaly and no transposition.
Relation per crib: CApos(c) = PApos(p) + key[idx mod P] (mod 26).
 conv 'carved': cribs sit at the official CARVED positions; a dropped letter at true index d shifts the key index of
                every carved letter at or after d by +1 (del), an extra carved letter at d is junk and shifts later ones by -1 (ins).
 conv 'plain' : cribs sit at the official PLAINTEXT positions of a 98-/96-letter plaintext; the carved letter paired with
                plaintext j is j - [j>d] (del; j==d lost) or j + [j>=d] (ins); key index = j.
 'chg': one crib letter dropped (a changed carved letter under a crib).
Only distinct constraint patterns are solved. UNSAT = impossible. Usage: python3 anomaly_sat.py [K4|null:SEED|control]"""
import sys, random, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from kryptos_text import K4
CR = [(21+i, c) for i, c in enumerate("EASTNORTHEAST")] + [(63+i, c) for i, c in enumerate("BERLINCLOCK")]
ALLTAGS = {}
def patterns():
    pats = {}
    def add(tag, lst):   # lst of (carved_idx, plain_letter, key_idx); first tag represents the pattern
        pats.setdefault(tuple(lst), tag); ALLTAGS.setdefault(tuple(lst), []).append(tag)
    add("none", [(i, p, i) for i, p in CR])
    for d in range(98):   # del, carved convention
        add(f"del-carved d={d}", [(i, p, i + (i >= d)) for i, p in CR])
        L = []
        for j, p in CR:
            if j == d: continue
            L.append((j - (j > d), p, j))
        add(f"del-plain d={d}", L)
    for d in range(97):
        add(f"ins-carved d={d}", [(i, p, i - (i > d)) for i, p in CR if i != d])
        add(f"ins-plain d={d}", [(j + (j >= d), p, j) for j, p in CR])
    for k in range(24):
        add(f"chg crib#{k}", [(i, p, i) for n, (i, p) in enumerate(CR) if n != k])
    return pats
def model(CT, lst, P):
    pool = IDPool(); cl = []
    def onehot(name):
        v = [pool.id((name, x)) for x in range(26)]; cl.extend(CardEnc.equals(v, 1, vpool=pool, encoding=EncType.seqcounter).clauses); return v
    pl = sorted(set(p for _, p, _ in lst)); cs = sorted(set(CT[i] for i, _, _ in lst))
    pa = {c: onehot(("pa", c)) for c in pl}; ca = {c: onehot(("ca", c)) for c in cs}
    for v in range(26):
        for grp in ([pa[c][v] for c in pl], [ca[c][v] for c in cs]):
            cl.extend(CardEnc.atmost(grp, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
    cl.append([pa[pl[0]][0]])
    key = [onehot(("k", r)) for r in range(P)]
    for i, p, k in lst:
        for u in range(26):
            for w in range(26): cl.append([-pa[p][u], -key[k % P][w], ca[CT[i]][(u + w) % 26]])
    with Cadical153(bootstrap_with=cl) as s: return s.solve()
def run(CT, Pmax=26):
    pats = patterns(); res = {}
    for P in range(1, Pmax+1):
        sat = [tag for lst, tag in pats.items() if model(CT, list(lst), P)]
        res[P] = sat; print(f"P={P}: {len(sat)}/{len(pats)} patterns SAT" + (f"  {sat}" if sat else ""), flush=True)
    return res
if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "K4"; Pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    if a == "K4": CT = K4
    elif a.startswith("null:"):
        l = list(K4); random.Random(int(a[5:])).shuffle(l); CT = "".join(l)
    else:   # control: random alphabets, period 7 key, plaintext of 98 letters, letter dropped at d=50 (carved conv.)
        r = random.Random(7); A = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); PA = A[:]; CAl = A[:]; r.shuffle(PA); r.shuffle(CAl)
        pt = ("SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAITEDX")
        key = [r.randrange(26) for _ in range(7)]; d = 50
        tru = [CAl[(PA.index(ch) + key[j % 7]) % 26] for j, ch in enumerate(pt)]   # true CT, 98 letters, cribs at carved pos
        # carved conv: carved i<d is tru[i], carved i>=d is tru[i+1]; build plaintext so cribs land at carved positions
        pt2 = list(pt); CT = "".join(tru[:d] + tru[d+1:])[:97]
        # cribs at carved 63-73 correspond to true 64-74: re-encrypt so that is consistent
        full = list("SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTHX" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT")
        tru = [CAl[(PA.index(ch) + key[j % 7]) % 26] for j, ch in enumerate(full)]; CT = "".join(tru[:d] + tru[d+1:])
        assert len(CT) == 97
        print("CONTROL: random PA/CA, period 7, true index 50 dropped from carving (carved convention)")
    t = time.time(); run(CT, Pmax); print(f"time {time.time()-t:.0f}s")

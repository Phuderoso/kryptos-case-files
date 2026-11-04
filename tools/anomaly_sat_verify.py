"""Extract and independently verify one SAT witness (anomaly_sat model): python3 sat_verify.py 'del-plain d=30' 6"""
import sys
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import anomaly_sat as S
from kryptos_text import K4
tag, P = sys.argv[1], int(sys.argv[2])
pats = S.patterns(); lst = [l for l, t in pats.items() if t == tag][0]
pool = IDPool(); cl = []
def onehot(name):
    v = [pool.id((name, x)) for x in range(26)]; cl.extend(CardEnc.equals(v, 1, vpool=pool, encoding=EncType.seqcounter).clauses); return v
pl = sorted(set(p for _, p, _ in lst)); cs = sorted(set(K4[i] for i, _, _ in lst))
pa = {c: onehot(("pa", c)) for c in pl}; ca = {c: onehot(("ca", c)) for c in cs}
for v in range(26):
    for grp in ([pa[c][v] for c in pl], [ca[c][v] for c in cs]): cl.extend(CardEnc.atmost(grp, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
key = [onehot(("k", r)) for r in range(P)]
for i, p, k in lst:
    for u in range(26):
        for w in range(26): cl.append([-pa[p][u], -key[k % P][w], ca[K4[i]][(u + w) % 26]])
with Cadical195(bootstrap_with=cl) as s:
    assert s.solve(); m = set(x for x in s.get_model() if x > 0)
val = lambda vs: [x for x in range(26) if vs[x] in m][0]
PA = {c: val(pa[c]) for c in pl}; CA = {c: val(ca[c]) for c in cs}; KEY = [val(k) for k in key]
assert len(set(PA.values())) == len(PA) and len(set(CA.values())) == len(CA)
ok = all((PA[p] + KEY[k % P]) % 26 == CA[K4[i]] for i, p, k in lst)
print(tag, "P=%d" % P, "witness verified:", ok, "| PApos", PA, "| CApos", CA, "| key", KEY)

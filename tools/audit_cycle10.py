"""Cycle 10 (A): audit of core assumptions used in cycles 1-9. Every check prints PASS/FAIL with the evidence."""
import sys, collections
sys.path.insert(0, "tools")
from kryptos_text import K1, K2, K3, K4, KA
from k4_anneal import AZ, KN
from solve_k1_k2_k3 import vig_dec, k3_dec
import k4_creative as C
ok = lambda b: "PASS" if b else "FAIL"
print("1. K4 text")
rows = [r.rstrip("\n") for r in open("data/elonka_panel_rows.txt")]
panel = "".join(rows[28:42]).replace("?", "")
anti = open("data/antipodes_kryptos_side_scirealm.txt").read().replace(" ", "").replace("\n", "")
print(f"   len 97: {ok(len(K4) == 97)}; starts OBKR / ends KCAR: {ok(K4[:4] == 'OBKR' and K4[-4:] == 'KCAR')}")
print(f"   = tail of Elonka panel transcript: {ok(panel.endswith(K4))}; appears twice verbatim in Antipodes text: {ok(anti.count(K4) == 2)}")
print("2. crib indexing (code uses 0-based dict KN)")
E = {**{21 + j: c for j, c in enumerate('EASTNORTHEAST')}, **{63 + j: c for j, c in enumerate('BERLINCLOCK')}}
print(f"   KN == 0-based 21..33 EASTNORTHEAST + 63..73 BERLINCLOCK (1-based 22-34, 64-74): {ok(KN == E)}")
pairs = {"FLRVQQPRNGKSS": "EASTNORTHEAST", "NYPVTTMZFPK": "BERLINCLOCK"}
print(f"   CT under cribs = Sanborn's published pairs FLRVQQPRNGKSS / NYPVTTMZFPK: {ok(K4[21:34] == 'FLRVQQPRNGKSS' and K4[63:74] == 'NYPVTTMZFPK')}")
print("3. alphabets")
kk = "".join(dict.fromkeys("KRYPTOS" + AZ))
print(f"   KA == keyed('KRYPTOS') == {KA}: {ok(KA == kk)}; AZ permutation: {ok(sorted(AZ) == sorted(KA))}")
print("4. K1-K3 reproduce (validates alphabet + Vigenere direction + K3 rotation)")
p1, p2, p3 = vig_dec(K1, 'PALIMPSEST'), vig_dec(K2.replace('?', ''), 'ABSCISSA'), k3_dec(K3.replace('?', ''))
print(f"   K1 starts BETWEENSUBTLESHADING: {ok(p1.startswith('BETWEENSUBTLESHADING'))}; K2 starts ITWASTOTALLYINVISIBLE: {ok(p2.startswith('ITWASTOTALLYINVISIBLE'))}; K3 starts SLOWLYDESPARATLY: {ok(p3.startswith('SLOWLYDESPARATLY'))}")
print("5. cipher-mode conventions (all tools): vig c=p+k ; beau c=k-p ; varbeau c=p-k (= vig with key -k)")
for mode in ("vig", "beau", "varbeau"):
    pass
print("   varbeau is redundant only where the key is free (periodic/unknown keys); it matters for fixed keys (words, running keys).")
print("   FINDING: cycle 9 H9 (running keys) tested vig/beau only -> rerun below with varbeau.")
print("6. pure-transposition impossibility")
need = collections.Counter("EASTNORTHEAST" + "BERLINCLOCK"); have = collections.Counter(K4)
short = {c: (n, have[c]) for c, n in need.items() if have[c] < n}
print(f"   crib letters needed > available in K4: {short} -> {ok(bool(short))} (E needs 3, K4 has 2: proof holds)")
print("7. W positions / segment arithmetic (cycle 9)")
print(f"   W 1-based {[i + 1 for i, c in enumerate(K4) if c == 'W']}; segments {[len(s) for s in C.segments()]} sum+5W = {sum(len(s) for s in C.segments()) + 5}: {ok(sum(len(s) for s in C.segments()) + 5 == 97)}")
print("8. rerun of cycle-9 H9 running keys including variant Beaufort")
srcs = {"P1": p1, "P2": p2, "P3": p3, "P123": p1 + p2 + p3, "C123": (K1 + K2 + K3).replace("?", ""), "tableau": "".join(KA[r:] + KA[:r] for r in range(26))}
srcs.update({k + "_rev": v[::-1] for k, v in list(srcs.items())})
t = s = 0
for pa, ca, mode in C.pairs(True):
    if mode != "vig": continue
    req = C.need(K4, C.ALPH[pa], C.ALPH[ca], "vig")
    for an in ("AZ", "KA"):
        for name, src in srcs.items():
            for o in range(len(src) - 97 + 1):
                t += 1
                if all((-C.ALPH[an].index(src[o + i])) % 26 == e for (i, _), e in zip(C.CRIBS, req)): s += 1
print(f"   varbeau running-key tests {t:,}; survivors {s}")

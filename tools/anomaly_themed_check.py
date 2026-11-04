"""Cycle 24: test the SAT-surviving anomaly patterns (K4, P=6 and P=7) against 86,731 themed keyword alphabets
(cycle 11 set: AZ, KA, keyed/reversed/columnar alphabets of plain-sight words and two-word phrases) as Quagmire III
(same alphabet both sides), II (AZ plain) and I (AZ cipher), Vigenere-type and Beaufort."""
import numpy as np, os
from kryptos_text import K4
import anomaly_sat as S
A = np.fromfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "alpha.bin") if os.path.exists("../data/alpha.bin") else "/workspace/kcl/data/alpha.bin", dtype=np.uint8).reshape(-1, 26)
inv = np.argsort(A, axis=1); AZi = np.tile(np.arange(26), (len(A), 1))
pats = {t: l for l, t in S.patterns().items()}
SURV = {6: ['del-plain d=30', 'del-plain d=31', 'del-plain d=32', 'del-plain d=33', 'del-plain d=34', 'del-plain d=63', 'del-plain d=64',
            'del-plain d=65', 'ins-plain d=31', 'ins-plain d=32', 'ins-plain d=33', 'ins-plain d=65', 'ins-plain d=34', 'ins-plain d=64'],
        7: ['del-carved d=66']}
tot = 0
for P, tags in SURV.items():
    for tag in tags:
        lst = pats[tag]; ci = np.array([ord(K4[i]) - 65 for i, _, _ in lst]); pi = np.array([ord(p) - 65 for _, p, _ in lst])
        ki = np.array([k % P for *_, k in lst]); n = 0
        for mode in (0, 1):
            for kind in ("QIII", "QII", "QI"):
                PAi = AZi if kind == "QII" else inv; CAi = AZi if kind == "QI" else inv
                kv = (CAi[:, ci] - PAi[:, pi]) % 26 if mode == 0 else (CAi[:, ci] + PAi[:, pi]) % 26
                ok = np.ones(len(A), bool)
                for r in range(P):
                    m = ki == r
                    if m.sum() > 1: ok &= (kv[:, m] == kv[:, m][:, [0]]).all(axis=1)
                n += int(ok.sum())
        tot += n; print(f"P={P} {tag}: themed-alphabet hits {n}")
print(f"alphabets {len(A)}; total hits {tot}")

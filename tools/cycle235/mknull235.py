"""Fresh shuffled nulls (PREREG235): set A 209647-209658, set B 209659-209670; random.Random(seed).shuffle(list(K4)).
Writes nulls235.tsv: seed set text sha256"""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls235.tsv', 'w') as fh:
    for s in range(209647, 209671):
        L = list(K4); random.Random(s).shuffle(L); t = ''.join(L)
        fh.write(f"{s}\t{'A' if s < 209659 else 'B'}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()}\n")

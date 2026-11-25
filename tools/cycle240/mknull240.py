"""Fresh nulls (PREREG240): set A 209719-209724, set B 209725-209730; random.Random(seed).shuffle(list(K4)), as mknull235.py."""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls240.tsv', 'w') as fh:
    for s in range(209719, 209731):
        t = list(K4); random.Random(s).shuffle(t); t = ''.join(t)
        fh.write(f"{s}\t{'A' if s < 209725 else 'B'}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()[:16]}\n")
